from PIL import Image 
from PIL.ExifTags import TAGS, GPSTAGS 
import sys

def print_exif(imageName):
   image = Image.open(imageName) 
   info = image._getexif() 
   if info:
     for tag, value in info.items(): 
         key = TAGS.get(tag, tag) 
         print(key + " " + str(value))

print_exif(sys.argv[1])
