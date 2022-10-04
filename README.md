# COMP8505_ASG1

## COMP 8505 - Assignment 1

A simple LSB steganographic application that:
- calculates the secret data and cover file size to ascertain that the cover file is large enough to hold all the secret data
- encrypts secret data using symmetric algorithm
- encodes and embeds secret data into the cover image
- decodes and extracts secret data from the cover image
- decrypts secret data using symmetric algorithm

### Install Pillow and cryptography using the commands:

```pip install pillow```

```pip install cryptography```

### For help function:

```python stego.py -h```

```python stego.py --help```

### To encrypt and encode:

```python stego.py -e [path to secret data file] cover.bmp```

### To decode and extract:

```python stego.py -d [directory to modified image] mod.bmp```

### To decrypt:

```python [path to encrypted file]```

### Symmetric Algorithm

- [Encrypt and Decrypt Files using Python](https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/)
