#!/usr/bin/python
# ---------------------------------------------------------------------------------------
# --	SOURCE FILE:	dcutils.py -    The file that contains the functions related to encryption and decryption.
# --                                    Main file is dcstego.py.
# --
# --	DATE:			October 10, 2021
# --
# --	REVISIONS:		N/A
# --
# --	DESIGNERS:		William Prout
# --
# --	PROGRAMMERS:	William Prout
# --
# --	NOTES:
# --    encryptSecretImage(secret_image_name, password):
# --    The function opens the secret image and reads its data and adds the file name to the front of the bytes string.
# --    The function encrypts the byte string using AES encryption using the input password.
# --    The function combines the 'nonce' output by the encryption libary function and the cipher into one bytes string.
# --    The function returns the combined cipher bytes string. 
# --
# --    decryptSecretImage(cipher, password):
# --    The function extracts the 'nonce' required for decryption from the cipher input.
# --    The function extracts the actual cipher from the cipher input as well.
# --    The function decrypts the cipher using AES decryption using the input password.
# --    The image data and the original file name are extracted from the decrypted data.
# --    The image data is written to the image file corresponding to the original file name.
# --
# --    SCRIPT EXECUTION:
# --    python covert.py encrypt [secret image] [cover image] [output image]
# --    python covert.py decrypt [stego image]
# --
# ---------------------------------------------------------------------------------------


import sys
from Crypto.Cipher import AES
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
        print("Saved decrypted image:", filename)
        write_image.close()
