#!/usr/bin/python
# ---------------------------------------------------------------------------------------
# --	SOURCE FILE:	dcstego.py -    The main file of a bash script that embeds an image into a cover image using the LSB stegonography technique.
# --                                    The script can also extract the original image from the encoded image. 
# --                                    The encoded data is also encrypted/decrypted using a user provided password.
# --                                    Additional python files that contain the imported functions are 'dcimage.py' and 'dcutils.py'
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
# --    Encrypt mode:
# --    The program will verify that the source and cover image are compatible. The cover image must be at least 8 times larger than the source image.
# --	The program will open and encrypt the source image data.
# --	The program will encode the cover image with the encrypted data using the LSB method.
# --    The program will save the encoded image to the system.
# --
# --    Decrypt mode:
# --    The program will extract and then decrypt the encrypted data from the image.
# --    The program will save the original image file to the system.
# --
# --
# --    SCRIPT EXECUTION:
# --    python covert.py encrypt [secret image] [cover image] [output image]
# --    python covert.py decrypt [stego image]
# --
# ---------------------------------------------------------------------------------------

import sys
from dcimage import getImageDimensions, stegoEncode, stegoDecode
from dcutils import encryptSecretImage, decryptSecretImage
import getpass

syntaxMessage = '''Please provide parameters in the following syntax:
                python covert.py encrypt [secret image] [cover image] [output image]
                python covert.py decrypt [stego image]
                '''

if ((len(sys.argv) == 5) and (sys.argv[1] == "encrypt")):
    mode = sys.argv[1]
    secret_image_name = sys.argv[2]
    cover_image_name = sys.argv[3]
    output_image_name = sys.argv[4]
elif ((len(sys.argv) == 3) and (sys.argv[1] == "decrypt")):
    mode = sys.argv[1]
    stego_image_name = sys.argv[2]
else:
    print(syntaxMessage)
    exit()

# password = getpass.getpass('Please enter a password:')

if mode == "encrypt":
    try:
        secret_width, secret_height = getImageDimensions(secret_image_name)
        secret_pixel_count = secret_width * secret_height
    except:
        print("Secret image could not be read.")

    try:
        cover_width, cover_height = getImageDimensions(cover_image_name)
        cover_pixel_count = cover_width * cover_height
    except:
        print("Cover image could not be read.")

    print("Secret image:", secret_image_name)
    print("Cover image:", cover_image_name)
    
    if ((cover_pixel_count / secret_pixel_count) > 8.2):
        print("Image sizes compatible, cover image is", str(cover_pixel_count / secret_pixel_count), 'times larger than the secret image.')

        #Encrypting
        cipher = encryptSecretImage(secret_image_name)

        # Writing to output image
        stegoEncode(cipher, cover_image_name, output_image_name)


elif mode == "decrypt":
    #Read from encrypted image
    cipher = stegoDecode(stego_image_name)

    #Decrypt cipher and save the revealed image
    decryptSecretImage(cipher)
