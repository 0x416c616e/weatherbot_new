#!/usr/bin/env python3
#Adds a timestamp to an image

import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
import argparse
import asio
import datetime

def main():
    #filename, date, text, color, size
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--filename', help='name of the image file to add the date to')
    parser.add_argument('--text', help='add an additional message after the timestamp')
    parser.add_argument('--size', help='set the size of the text to be put on the image')
    args = parser.parse_args()
    filename = str(args.filename)
    print("Filename: " + filename)
    if (asio.does_not_exist(filename)):
        print("Error: file with filename " + filename + " does not exist")
        print("How to use this program: image.py --filename=photo.jpg")
        print("Optionally: image.py --filename=photo.jpg --text='this line will go under the date'")
        print("Optionally specify the size, i.e. image.py --size=32")
        print("Use image.py --help for help")
        sys.exit(1)
    else:
        today = datetime.datetime.now()
        formatted_date = today.strftime("%A, %B %d, %Y %I:%M%p")
        full_message = formatted_date
        if (args.text != ""):
            full_message += "\n" + str(args.text)
        print("Full message: " + str(full_message))
        photo = Image.open(filename)
        photodraw = ImageDraw.Draw(photo)
        fontsize = ""
        if (args.size == ""):
            fontsize = 64
        else:
            fontsize = int(args.size)
        myfont = ImageFont.truetype("/home/alan/twitterweatherbot/pt-sans.ttf", fontsize)
        photodraw.text((10,10), full_message, fill=(255,0,0), font=myfont)
        photo.save(filename)
        photo.close()
        




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nQuitting. Goodbye.")
        sys.exit()
