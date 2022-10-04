#!/usr/bin/env python

###########################################################################################
# FILE
#
#   Name:  image.py
#
#   Developer:  Eunsaem Lee
#
#   Date:       2022-10-04
#
#   Description:
#     This file handles image processing and manipulation.
#
###########################################################################################

# Imports PIL module
from PIL import Image

###########################################################################################
# FUNCTION
#
#   Name:  check_encode
#
#   Parameters:
#     minsize   - minimum number of bytes that the image can encode
#     imgpath   - path of the image
#
#   Returns:
#     True      - image CAN encode the minimum number of bytes
#     False     - image CANNOT encode the minimum number of bytes
#     exception - image file could not be opened
#
#   Description:
#     Determines whether the image can encode at least minsize bytes. If not, prints an 
#     error message.
#
###########################################################################################
def check_encode(minsize, imgpath):
    try:
        cover = Image.open(imgpath, 'r')
    except:
        print("Could not open image: {}".format(imgpath))
    
    width, height = cover.size

    # RGB
    bytesize = width * height * 3

    cover.close()

    if bytesize < minsize:
        print("The image is too small to fit the data: image size is {} bytes but minimum required is {} bytes.".format(cover.size, minsize))
        return False
    
    return True

###########################################################################################
# FUNCTION (GETTER)
#
#   Name:  get_pixel
#
#   Parameters:
#     imgpath   - path of the image
#
#   Returns:
#     array     - array of a pixel buffer + Image object
#     exception - image file could not be opened
#
#   Description:
#     Opens the image and gets a buffer of its pixels for writing. If not, prints an error 
#     message.
#
###########################################################################################
def get_pixel(imgpath):
    try:
        img = Image.open(imgpath, 'r')
    except:
        print("Could not open image: {}".format(imgpath))
    
    return (bytearray(img.tobytes()), img)

###########################################################################################
# FUNCTION (SETTER)
#
#   Name:  set_pixel
#
#   Parameters:
#     pixel     - pixel to save as an image
#     img       - Image object from get_pixel
#     dstpath   - destination path of the image
#
#   Returns:
#     exception - image file could not be saved
#
#   Description:
#     Saves the pixels to the destination path with the same cover image format. If not, 
#     prints an error message.
#
###########################################################################################
def set_pixel(pixel, img, dstpath):
    try:
        im = Image.frombytes(img.mode, img.size, pixel)
        im.save(dstpath, img.format)
    except Exception as error:
        print("Could not save image to: {}".format(dstpath))
