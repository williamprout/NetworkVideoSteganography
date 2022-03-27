#!/usr/bin/python

import sys
from dnacryptograpy import DNAencrypt, DNAdecrypt

def encryptSecretImage(secret_image_name, key):
    with open(secret_image_name, "rb") as image:
            #Read image data in binary
            # print("Reading secret image...")
            secret_image_bytes = bytes(image.read())
            image.close()
            secret_image_name_bytes = str.encode(secret_image_name)
            payload = secret_image_name_bytes + secret_image_bytes

    # Convert password to 16 bytes
    # password = bytes(password, 'utf-8')
    # key = password + bytes(16 - len(password))
    # cipher = AES.new(key, AES.MODE_EAX)
    # nonce = cipher.nonce
    # print("Encrypting secret image and original filename...")
    # ciphertext, tag = cipher.encrypt_and_digest(payload)

    final_payload = payload
    raw_data = bin(int.from_bytes(final_payload, byteorder=sys.byteorder))[2:]
    cipher = DNAencrypt(key, raw_data)
    return(cipher)


def decryptSecretImage(cipher, key):
    # password = bytes(password, 'utf-8')
    # password = password + bytes(16 - len(password))
    # key = password

    plaintext = DNAdecrypt(key, cipher)
    
    def bitstring_to_bytes(s):
        return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')

    plaintext = bitstring_to_bytes(str(plaintext))
    
    # nonce = (plaintext[0:(plaintext.rfind(bytes('\\nonce\\', 'utf-8')))])
    # plaintext = plaintext[(plaintext.rfind(bytes('\\nonce\\', 'utf-8')) + 7):]

    # cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    # print("Decrypting secret image and original filename...")
    try:
        # plaintext = cipher.decrypt(plaintext)
        filename = (plaintext[0:(plaintext.rfind(bytes('.bmp', 'utf-8')) + 4)]).decode('utf-8')
        plaintext = plaintext[(plaintext.rfind(bytes('.bmp', 'utf-8')) + 4):]
    except:
        print("Decryption failed.")
        return None


    with open(filename, "wb") as write_image:
        write_image.write(plaintext)
        # print("Saved decrypted image:", filename)
        write_image.close()
