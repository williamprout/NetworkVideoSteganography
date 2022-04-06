#!/usr/bin/python

import sys
from dnacryptograpy import DNAencrypt, DNAdecrypt

def encryptSecretImage(secret_image_name, key):
    with open(secret_image_name, "rb") as image:
            #Read image data in binary
            secret_image_bytes = bytes(image.read())
            image.close()
            secret_image_name_bytes = str.encode(secret_image_name)
            payload = secret_image_name_bytes + secret_image_bytes

    final_payload = payload
    raw_data = bin(int.from_bytes(final_payload, byteorder=sys.byteorder))[2:]
    cipher = DNAencrypt(key, raw_data)
    return(cipher)


def decryptSecretImage(cipher, key):
    plaintext = DNAdecrypt(key, cipher)
    
    def bitstring_to_bytes(s):
        return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')

    plaintext = bitstring_to_bytes(str(plaintext))
    

    try:
        filename = (plaintext[0:(plaintext.rfind(bytes('.bmp', 'utf-8')) + 4)]).decode('utf-8')
        plaintext = plaintext[(plaintext.rfind(bytes('.bmp', 'utf-8')) + 4):]
    except:
        print("Decryption failed.")
        return None


    with open(filename, "wb") as write_image:
        write_image.write(plaintext)
        write_image.close()
