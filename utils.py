#!/usr/bin/env python

###########################################################################################
# FILE
#
#   Name:  utils.py
#
#   Developer:  Eunsaem Lee
#
#   Date:       2022-10-04
#
#   Description:
#     This file handles data hiding and extraction.
#
###########################################################################################

import os

MASKS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

###########################################################################################
# FUNCTION
#
#   Name:  encode_byte
#
#   Parameters:
#     srcbyte   - byte to be encoded
#     dstbytes  - bytes which will contain byte to be encoded
#     dstoffset - offset into dstbytes at which to start encoding:
#                 len(dstbytes) - dstoffset >= 8
#
#   Returns:
#     offset    - offset to start encoding another byte
#
#   Description:
#     Splits srcbyte into bits and encodes them into the least significant bits of 8 bytes
#     in dstbytes, starting at dstoffset.
#
###########################################################################################
def encode_byte(srcbyte, dstbytes, dstoffset):
    for i in range(8):
        mask = MASKS[i]
        bit = (srcbyte & mask) >> (7 - i)

        byte = dstbytes[dstoffset + i]
        byte &= 0xFE    # zero the last
        byte |= bit     # set the last bit

        dstbytes[dstoffset + i] = byte

    return dstoffset + 8

###########################################################################################
# FUNCTION
#
#   Name:  decode_byte
#
#   Parameters:
#     srcbytes  - bytes with encoded data
#     srcoffset - offset into srcbytes at which to start decoding:
#                 len(srcbytes) - srcoffset >= 8
#
#   Returns:
#     result    - decoded byte
#     offset    - offset to start decoding another byte
#
#   Description:
#     Constructs a byte from the least significant bits of 8 bytes in srcbytes, starting at
#     srcoffset.
#
###########################################################################################
def decode_byte(srcbytes, srcoffset):
    result = 0

    for i, byte in enumerate(srcbytes[srcoffset:srcoffset + 8]):
        bit = byte & 0x01
        result |= bit << (7 - i)

    return (result, srcoffset + 8)

###########################################################################################
# FUNCTION
#
#   Name:  encode_filename
#
#   Parameters:
#     filename  - name of file to encode; must be <= 255 bytes
#     dstbytes  - bytes with will contain encoded name of file
#
#   Returns:
#     offset    - offset to start encoding the data
#
#   Description:
#     Encodes the length of filename and filename into the least significant bits of first 
#     (8 + 8 * len(filename)) bytes in dstbytes.
#
###########################################################################################
def encode_filename(filename, dstbytes):
    namesize = len(filename)
    offset = encode_byte(namesize, dstbytes, 0)

    for char in filename:
        byte = ord(char)
        offset = encode_byte(byte, dstbytes, offset)

    return offset

###########################################################################################
# FUNCTION
#
#   Name:  decode_filename
#
#   Parameters:
#     srcbytes  - bytes that contain the encoded name of file
#
#   Returns:
#     offset    - offset to start encoding the data
#
#   Description:
#     Decodes a file name that is encoded in srcbytes, starting at byte = 0.
#
###########################################################################################
def decode_filename(srcbytes):
    name = ""
    namesize, offset = decode_byte(srcbytes, 0)

    offset = 8

    for i in range(namesize):
        char, offset = decode_byte(srcbytes, offset)
        name += chr(char)

    return (name, offset)

###########################################################################################
# FUNCTION
#
#   Name:  encode_file
#
#   Parameters:
#     srcpath   - path to the file to encode
#     dstbytes  - buffer which will contain encoded file
#
#   Returns:
#     None.
#
#   Description:
#     Encodes the file in srcpath to dstbytes using least significant bit (LSB) 
#     steganography.
#
###########################################################################################
def encode_file(srcpath, dstbytes):
    filename = os.path.basename(srcpath)
    filesize = os.path.getsize(srcpath)

    with open(srcpath, 'rb') as payload:
        offset = encode_filename(filename, dstbytes)
        filesizebytes = [(filesize & 0xFF0000) >> 16, (filesize & 0x00FF00) >> 8, filesize & 0x0000FF]

        for byte in filesizebytes:
            offset = encode_byte(byte, dstbytes, offset)

        try:
            strbyte = payload.read(1)
        except:
            print("Failed to read from source file.")

        while len(strbyte) != 0:
            byte = ord(strbyte)
            offset = encode_byte(byte, dstbytes, offset)

            try:
                strbyte = payload.read(1)
            except:
                print("Failed to read from source file.")

###########################################################################################
# FUNCTION
#
#   Name:  decode_file
#
#   Parameters:
#     srcbytes  - buffer with encoded data
#
#   Returns:
#     filename  - decoded filename
#     contents  - decoded file contents in bytearray
#
#   Description:
#     Decodes the file in srcbytes using least significant bit (LSB) steganography.
#
###########################################################################################
def decode_file(srcbytes):
    filename, offset = decode_filename(srcbytes)

    contents = bytearray()
    filesize = 0

    for i in range(3):
        filesizebyte, offset = decode_byte(srcbytes, offset)
        filesize += filesizebyte << ((2 - i) * 8)
    
    for i in range(filesize):
        byte, offset = decode_byte(srcbytes, offset)
        contents.append(byte)
    
    return (filename, contents)
