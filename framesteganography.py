#!/usr/bin/python

from PIL import Image
import numpy as np

def getImageDimensions(image_name):
    with Image.open(image_name) as img:
        if img.format != 'BMP':
            raise Exception(image_name + " must be .bmp format.")
        width, height = img.size
        return(width, height)

def stegoEncode(secret, cover, output):
    # Writing to encrypted image
    cover_image = Image.open(cover)
    cover_image.save(output) 
    
    output_image = Image.open(cover)
    # output_rgb = output_image.convert("RGB")
    width, height = output_image.size

    # pixels = output_rgb.load()
    
    data = np.asarray(output_image)

    #Embedding main payload at the beginning of the file
    # print("Manipulating cover image to store encrypted data...")
    i = 0
    finished = False
    # print(output, "start")
    for y in range(height):
        for x in range(width):
            r, g, b = data[y, x]
            # print("regular(", x, y, ")" , r, g, b)
            # r2,g2,b2 = data[y,x]
            # print("numpy(", x, y,")", r2,g2,b2)
            
            # print(data)

            #Red pixel
            if i < len(secret):
                # r_bit = bin(r)
                # r_new_final_bit = secret[i]
                new_bit_red_pixel = int(bin(r)[:-1]+str(secret[i]), 2)
                i += 1
            #Green pixel
            if i < len(secret):
                # g_bit = bin(g)
                # g_new_final_bit = secret[i]
                new_bit_green_pixel = int(bin(g)[:-1]+str(secret[i]), 2)
                i += 1
            #Blue pixel
            if i < len(secret):
                # b_bit = bin(b)
                # b_new_final_bit = secret[i]
                new_bit_blue_pixel = int(bin(b)[:-1]+str(secret[i]), 2)
                i += 1

            if i <= len(secret):
                # output_rgb.putpixel((x, y), (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel))
                data[y, x] = (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel)
                if i >= len(secret):
                    i += 1
                    finished = True
                    break
        if finished:
            break
        
    # print(output, "end")

    bin_payload_length = bin(len(secret))[2:]
    # print("Embedding payload length at the end of the file")
    #Embedding payload length at the end of the file
    i = 0
    i = (len(bin_payload_length) - 1)
    while i >= 0:
        for x in range(width):
            if i >= 0:
                r, g, b = data[height-1, (width - x) - 1]
            #Red pixel
            if i >= 0:
                r_bit = bin(r)
                r_new_final_bit = bin_payload_length[i]
                new_bit_red_pixel = int(r_bit[:-1]+str(r_new_final_bit), 2)
                i -= 1
            else:
                r_bit = bin(r)
                r_new_final_bit = 0
                new_bit_red_pixel = int(r_bit[:-1]+str(r_new_final_bit), 2)
            #Green pixel
            if i >= 0:
                g_bit = bin(g)
                g_new_final_bit = bin_payload_length[i]
                new_bit_green_pixel = int(g_bit[:-1]+str(g_new_final_bit), 2)
                i -= 1
            else:
                g_bit = bin(r)
                g_new_final_bit = 0
                new_bit_green_pixel = int(g_bit[:-1]+str(g_new_final_bit), 2)
            #Blue pixel
            if i >= 0:
                b_bit = bin(b)
                b_new_final_bit = bin_payload_length[i]
                new_bit_blue_pixel = int(b_bit[:-1]+str(b_new_final_bit), 2)
                i -= 1
            else:
                b_bit = bin(r)
                b_new_final_bit = 0
                new_bit_blue_pixel = int(b_bit[:-1]+str(b_new_final_bit), 2)
            if i >= -3:
                data[height-1, (width - x) - 1] = (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel)
                # output_rgb.putpixel(((width - x) - 1, height-1), (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel))
                final_x = (width - x) - 1
                if i < 0: 
                    i = -10
                    break
    # print("Creating end buffer")
    #Creating an end buffer 
    j = 0
    x = final_x
    x -= 1
    while j < 9:
        r_bit = bin(r)
        r_new_final_bit = 0
        new_bit_red_pixel = int(r_bit[:-1]+str(r_new_final_bit), 2)
        j += 1
        g_bit = bin(g)
        g_new_final_bit = 0
        new_bit_green_pixel = int(g_bit[:-1]+str(g_new_final_bit), 2)
        j += 1
        b_bit = bin(b)
        b_new_final_bit = 0
        new_bit_blue_pixel = int(b_bit[:-1]+str(b_new_final_bit), 2)
        j += 1
        data[height-1, x] = (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel)   
        # output_rgb.putpixel((x, height-1), (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel))
        x -= 1
    output_rgb = Image.fromarray(data, 'RGB')
    output_rgb.save(output)
    # print("Encoding complete.")
    # print("Saved output image:", output)


def stegoDecode(stego_image_name):
    #GET INFO FROM SECRET IMAGE
    secret = Image.open(stego_image_name)
    secret_rgb = secret.convert("RGB")
    width, height = secret_rgb.size

    len_binary_string = ''
    zero_counter = 0
    while zero_counter < 9:
        for x in range(width):
            if zero_counter < 9:
                r, g, b = secret_rgb.getpixel(((width - x) - 1, height - 1))
            if zero_counter < 9:
                r_bit = bin(r)
                r_final_bit = int(r_bit[-1])
                len_binary_string = len_binary_string + str(r_final_bit)
                if r_final_bit == 0:
                    zero_counter += 1
                else:
                    zero_counter = 0
            if zero_counter < 9:
                g_bit = bin(g)
                g_final_bit = int(g_bit[-1])
                len_binary_string = len_binary_string + str(g_final_bit)
                if g_final_bit == 0:
                    zero_counter += 1
                else:
                    zero_counter = 0
            if zero_counter < 9:
                b_bit = bin(b)
                b_final_bit = int(b_bit[-1])
                len_binary_string = len_binary_string + str(b_final_bit)
                if b_final_bit == 0:
                    zero_counter += 1
                else:
                    zero_counter = 0

    payload_length = ''
    i = len(len_binary_string) - 1
    while i >= 0:
        payload_length = payload_length + len_binary_string[i]
        i-=1

    for i in payload_length:
        if i == '0':
            payload_length = payload_length[1:]
        else: 
            break
    
    payload_length = int(payload_length, 2)

    binary_string = ''
    i = 0
    # print("Manipulating secret image to retrieve encrypted data...")
    while i < payload_length:
        for y in range(height):
            for x in range(width):
    
                r, g, b = secret_rgb.getpixel((x, y))

                #Red pixel
                if i < payload_length:
                    r_bit = bin(r)
                    r_final_bit = int(r_bit[-1])
                    binary_string = binary_string + str(r_final_bit)
                    i += 1
            
                #Green pixel
                if i < payload_length:
                    g_bit = bin(g)
                    g_final_bit = int(g_bit[-1])
                    binary_string = binary_string + str(g_final_bit)
                    i += 1

                #Blue pixel
                if i < payload_length:
                    b_bit = bin(b)
                    b_final_bit = int(b_bit[-1])
                    binary_string = binary_string + str(b_final_bit)
                    i += 1

    # def bitstring_to_bytes(s):
    #     return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')

    # cipher = bitstring_to_bytes(str(binary_string))
    # print("Decoding complete.")
    return(binary_string)