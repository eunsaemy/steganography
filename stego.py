#!/usr/bin/env python

###########################################################################################
# FILE
#
#   Name:  stego.py
#
#   Developer:  Eunsaem Lee
#
#   Date:       2022-10-04
#
#   Description:
#     This file drives the LSB steganographic application that parses command line 
#     arguments, checks file sizes and file formats, etc.
#
###########################################################################################

import argparse
import os
import sys

# Imports Encryption module
import encryption
# Imports Image module
import image
# Imports Utils module
import utils

# 2^24 - 1
MAX_FILESIZE = 16777215

###########################################################################################
# FUNCTION (MAIN)
#
#   Name:  encode
#
#   Parameters:
#     None.
#
#   Returns:
#     None.
#
#   Description:
#     Determines whether the image can encode at least minsize bytes. If not, prints an 
#     error message.
#
###########################################################################################
def main():
    # Command line prompt
    # (help function that displays the application's switches and command line arguments)
    parser = argparse.ArgumentParser(description="LSB steganographic application")
    parser.add_argument("image", help="if -e is specified, it is the path to the cover image; if -d is specified, it is the path to the modified image; otherwise, it is the path to the file to decrypt")
    parser.add_argument("-e", "--infile", help="path to a file to encrypt and encode in the cover image")
    parser.add_argument("-d", "--outfile", help="directory to a folder to decode the modified image")

    args = parser.parse_args()

    # Encrypt and Encode
    if args.infile:
        if not os.path.exists(args.infile):
            print("No such file exists: {}".format(args.encode))
            sys.exit(1)
        elif not os.path.isfile(args.infile):
            print("{} must be a regular file but is either a directory of a special file".format(args.encode))
            sys.exit(1)

        srcname = os.path.basename(args.infile)
        srcsize = os.path.getsize(args.infile)

        if srcsize > MAX_FILESIZE:
            print("{} is too large; must be <= {} bytes, but it is {} bytes".format(args.infile, MAX_FILESIZE, srcsize))
            sys.exit(1)
        
        dstpath = args.infile + os.path.splitext(args.image)[1]
        srcdir = os.path.dirname(args.infile)

        # The minimum number of bytes in the image to store
        # * the file name size (1 byte) and the file size (3 bytes)
        # * the file name
        # * the file's contents
        minsize = 32 + (8 * len(srcname)) + (8 * srcsize)

        success = True
        cover = None

        try:
            if image.check_encode(minsize, args.image):
                # encrypt the data
                encryption.generate(srcdir)
                encryption.encrypt(args.infile, srcdir)

                # encode the encrypted data
                pixels, cover = image.get_pixel(args.image)
                utils.encode_file(args.infile, pixels)
                image.set_pixel(bytes(pixels), cover, dstpath)
            else:
                success = False
        except Exception as error:
            print(str(error))
            success = False
        finally:
            if cover:
                cover.close()

        if not success:
            sys.exit(1)

        print("Successfully saved the modified image!")

    # Decode
    elif args.outfile:
        success = True
        modified = None

        try:
            pixels, modified = image.get_pixel(args.image)
            filename, contents = utils.decode_file(pixels)
            dstpath = os.path.join(args.outfile, filename)

            with open(dstpath, 'wb') as out:
                out.write(contents)
        except Exception as error:
            print(str(error))
            success = False
        finally:
            if modified:
                modified.close()

        print("Successfully decoded the modified image!")

        if not success:
            sys.exit(1)

    # Decrypt
    else:
        success = True

        dstpath = os.path.dirname(args.image)

        try:
            encryption.decrypt(args.image, dstpath)
        except Exception as error:
            print(str(error))
            success = False

        print("Successfully decrypted the decoded file!")

        if not success:
            sys.exit(1)

###########################################################################################
# FUNCTION (DRIVER)
#
#   Name:  encode
#
#   Parameters:
#     None.
#
#   Returns:
#     None.
#
#   Description:
#     Calls the main function.
#
###########################################################################################
if __name__ == "__main__":
    main()
