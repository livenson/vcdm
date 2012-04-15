import zlib
import struct
import os
import random

from Crypto.Cipher import AES


# (c) http://www.turnkeylinux.org/blog/python-symmetric-encryption
class CheckSumError(Exception):
    pass


def _lazysecret(secret, blocksize=32, padding='}'):
    """pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
        return secret + (blocksize - len(secret)) * padding
    return secret


def encrypt(plaintext, secret, lazy=True, checksum=True):
    """encrypt plaintext with secret
    plaintext   - content to encrypt
    secret      - secret to encrypt plaintext
    lazy        - pad secret if less than legal blocksize (default: True)
    checksum    - attach crc32 byte encoded (default: True)
    returns ciphertext
    """

    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)

    if checksum:
        plaintext += struct.pack("i", zlib.crc32(plaintext))

    return encobj.encrypt(plaintext)


def decrypt(ciphertext, secret, lazy=True, checksum=True):
    """decrypt ciphertext with secret
    ciphertext  - encrypted content to decrypt
    secret      - secret to decrypt ciphertext
    lazy        - pad secret if less than legal blocksize (default: True)
    checksum    - verify crc32 byte encoded checksum (default: True)
    returns plaintext
    """

    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)
    plaintext = encobj.decrypt(ciphertext)

    if checksum:
        crc, plaintext = (plaintext[-4:], plaintext[:-4])
        if not crc == struct.pack("i", zlib.crc32(plaintext)):
            raise CheckSumError("checksum mismatch")

    return plaintext


# Inspired by http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
def encrypt_file(key, in_fileobject, out_fileobject, chunksize=24 * 1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_fileobject:
            Input stream (file-like object)

        out_fileobject:
            Output stream

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    written_bytes = 0
    # reserve space for the written file size - we'll be able to write it only once the stream is closed
    out_fileobject.seek(struct.calcsize('Q'))
    out_fileobject.write(iv)

    while True:
        chunk = in_fileobject.read(chunksize)
        if len(chunk) == 0:
            break
        elif len(chunk) % 16 != 0:
            chunk += ' ' * (16 - len(chunk) % 16)
        written_bytes += len(chunk)
        out_fileobject.write(encryptor.encrypt(chunk))

    # write information about the total written number of bytes to the file header
    out_fileobject.seek(0)
    out_fileobject.write(struct.pack('<Q', written_bytes))


def decrypt_file(key, in_filename, out_fileobject, chunksize=24 * 1024):
    """ Decrypts a file using AES (CBC mode) with the given key.
    """
    with open(in_filename, 'rb') as infile:
        original_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        read_size = 0
        while read_size < original_size:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            else:
                read_size += len(chunk)
            out_fileobject.write(decryptor.decrypt(chunk))

        out_fileobject.truncate(original_size)
