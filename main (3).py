import numpy as np
from PIL import Image


def Encode(src, message, dest):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size // n

    message += "Stop"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels * 3:
        print("Error: file is too small")
        return

    index = 0
    for p in range(total_pixels):
        for q in range(0, 3):
            if index < req_pixels:
                # Изменяем последний бит с использованием корректного формата
                pixel_bin = format(array[p][q], '08b')
                new_pixel_bin = pixel_bin[:-1] + b_message[index]
                array[p][q] = int(new_pixel_bin, 2)
                index += 1

    array = array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)

    if '.' not in dest:
        dest += '.png'

    enc_img.save(dest)
    print("Image successfully зашифровано")



def Decode(src):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size // n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            # Извлекаем последний бит с использованием корректного формата
            pixel_bin = format(array[p][q], '08b')
            hidden_bits += pixel_bin[-1]

    hidden_bytes = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for byte in hidden_bytes:
        char = chr(int(byte, 2))
        message += char
        if message[-4:] == "Stop":
            break

    if "Stop" in message:
        print("Hidden message:", message[:-4])
    else:
        print("Hidden message not found")


def Stego():
    print("Choose option:")
    print("1: Encode")
    print("2: Decode")

    func = input()

    if func == '1':
        print("Enter the path to input image")
        src = input()
        print("Enter message to encode")
        message = input()
        print("Enter output file name")
        dest = input()
        Encode(src, message, dest)

    elif func == '2':
        print("Enter path to image with encoded message")
        src = input()
        Decode(src)

    else:
        print("Error: you enter wrong path")


Stego()
