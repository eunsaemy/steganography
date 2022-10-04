#!/usr/bin/env python

###########################################################################################
# FILE
#
#   Name:  encryption.py
#
#   Developer:  Eunsaem Lee
#
#   Date:       2022-10-04
#
#   Description:
#     This file handles data encryption and decryption.
#     It uses the symmetric algorithm to encrypt and decrypt the file.
#
###########################################################################################

# Imports Cryptography module
from cryptography.fernet import Fernet

import os

###########################################################################################
# FUNCTION
#
#   Name:  generate
#
#   Parameters:
#     dstpath   - path to store the key
#
#   Returns:
#     None.
#
#   Description:
#     Generates a key to encrypt and decrypt the file. If unable, prints an error message.
#
###########################################################################################
def generate(dstpath):
    key_name = 'filekey.key'
    name = os.path.join(dstpath, key_name)

    key = Fernet.generate_key()

    try:
        with open(name, 'wb') as filekey:
            filekey.write(key)
        
        print("Successfully generated the key: {}".format(key_name))
    except:
        print("Could not generate key: {}".format(key_name))

###########################################################################################
# FUNCTION
#
#   Name:  encrypt
#
#   Parameters:
#     filename  - name of the file to encrypt
#     dstpath   - path of the file to encrypt
#
#   Returns:
#     None.
#
#   Description:
#     Encrypts the file using the generated key. If unable, prints an error message.
#
###########################################################################################
def encrypt(filename, dstpath):
    key_name = 'filekey.key'
    name = os.path.join(dstpath, key_name)

    try:
        with open(name, 'rb') as filekey:
            key = filekey.read()
    except:
        print("Could not open encryption key: {}".format(key_name))

    fernet = Fernet(key)

    try:
        with open(filename, 'rb') as file:
            original = file.read()
    except:
        print("Could not open file: {}".format(filename))

    encrypted = fernet.encrypt(original)

    try:
        with open(filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        
        print("Successfully encrypted the file: {}".format(filename))
    except:
        print("Could not encrypt file: {}".format(filename))

###########################################################################################
# FUNCTION
#
#   Name:  decrypt
#
#   Parameters:
#     filename  - name of the file to decrypt
#     dstpath   - path of the file to decrypt
#
#   Returns:
#     None.
#
#   Description:
#     Decrypts the file using the generated key. If unable, prints an error message.
#
###########################################################################################
def decrypt(filename, dstpath):
    key_name = 'filekey.key'
    name = os.path.join(dstpath, key_name)

    try:
        with open(name, 'rb') as filekey:
            key = filekey.read()
    except:
        print("Could not open decryption key: {}".format(key_name))

    fernet = Fernet(key)

    try:
        with open(filename, 'rb') as enc_file:
            encrypted = enc_file.read()
    except:
        print("Could not open file: {}".format(filename))

    decrypted = fernet.decrypt(encrypted)

    try:
        with open(filename, 'wb') as dec_file:
            dec_file.write(decrypted)
        
        print("Successfully decrypted the file: {}".format(filename))
    except:
        print("Could not decrypt file: {}".format(filename))
