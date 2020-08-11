#!/usr/bin/env python3
# =================================================================================
# Name: mocr.py (Morse OCR)
# Version: v2 (alpha)
# Author: eauxfolles
# Date: 10.07.2020
# Description: Script to read morse code from file and translate into readable text
# Usage: "mocr.py <image>"
# Assumptions:  - Morse code expected to be reflected as "." and "-"
#               - "." expected to be 1 pixel, "-" expected to be 3 pixel long
#               - Image has consistent background color (as pixel at position 0,0)
#               - Background color is different than morse code
#               - Each line contains one word coded in morse
# =================================================================================

import sys
from PIL import Image

translate = {
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9',
    '-----': '0',
    '.-': 'a',
    '-...': 'b',
    '-.-.': 'c',
    '-..': 'd',
    '.': 'e',
    '..-.': 'f',
    '--.': 'g',
    '....': 'h',
    '..': 'i',
    '.---': 'j',
    '-.-': 'k',
    '.-..': 'l',
    '--': 'm',
    '-.': 'n',
    '---': 'o',
    '.--.': 'p',
    '--.-': 'q',
    '.-.': 'r',
    '...': 's',
    '-': 't',
    '..-': 'u',
    '...-': 'v',
    '.--': 'w',
    '-..-': 'x',
    '-.--': 'y',
    '--..': 'z',
    '.-.-.-': '.',
    '--..--': ',',
    '---...': ':',
    '-.-.-.': ';',
    '..--..': '?',
    '-.-.--': '!',
    '-....-': '-',
    '..--.-': '_',
    '-.--.': '(',
    '-.--.-': ')',
    '.----.': '\'',
    '.-..-.': '\"',
    '-...-': '=',
    '.-.-.': '+',
    '-..-.': '/',
    '.--.-.': '@'
}

# validate input provided with command line (has to be 2 parameters or "-help")
if len(sys.argv) < 2:
    print("error: no parameters provided")
    exit()
elif sys.argv[1] == "-help" or sys.argv[1] == "--help":
    print("usage: mocr.py <image-file>")
    exit()
elif len(sys.argv) == 2:
    image_file = sys.argv[1]
else:
    print("error: wrong number of parameters")
    exit()

# use module "PIL" (Python Image Library) to open image-file and load image-data (size and background color) 
try:
    morse_image = Image.open(image_file)
except:
    print("error: could not open file")
    exit()
width, height = morse_image.size
pixel_data = morse_image.load()
background_color = pixel_data[0,0]

# define function to translate morse character into letter
def morse_translate(morse_input):
    try:
        print(translate[morse_input], end = '')
    except:
        print("\nerror: unable to translate morse code")
        exit()

# loop through each pixel, line after line
for line in range(0, height):
    morse_char = ""
    pixel_count = 0
    morse_inline = 0
    for pixel in range(0, width):
        if pixel_data[pixel, line] != background_color:
            pixel_count += 1
            morse_inline = 1
        else:
            if pixel_count == 1:
                morse_char += "."
                if pixel_data[pixel+1, line] == background_color: 
                    morse_translate(morse_char)
                    morse_char = ""
            elif pixel_count == 3:
                morse_char += "-"
                if pixel_data[pixel+1, line] == background_color: 
                    morse_translate(morse_char)
                    morse_char = ""
            elif pixel_count == 0:
                pass
            else:
                print("error: cannot read morse code")
            pixel_count = 0
    if morse_inline != 0:
        print("")

# close image-file
morse_image.close()
