#!/usr/bin/env python3
#
#   ./grade.py : Grading automated scanned answer sheet:
#     ./grade.py form.jpg output.jpg output.txt 
# 
################################################################################
# CS B657 Spring 2019, Assignment #1 - Image Processing and Recognition Basics
#
# Completed by:
# Derrick Eckardt
# derrick@iu.edu
# 
# Completed on February 12, 2019. For the assignment details, please visit:
#
#   https://github.iu.edu/cs-b657-sp2019/derrick-a1/blob/master/a1.pdf
#
# For a complete details on this program, please visit the readme.md file at:
#
#   https://github.iu.edu/cs-b657-sp2019/derrick-a1/blob/master/README.md
#
################################################################################

# Import libraries
import sys
import PIL
import cProfile
from PIL import Image, ImageFilter
from collections import Counter
from pprint import pprint
import numpy as np
from timeit import timeit


def convolute(px):
    return px

def grade(form, output_im, output_file):
    print("Importing "+form+"...")
    # Set-up
    im = Image.open(form).convert('L').resize((850,1100))
    px = im.load()
    width = im.width
    height = im.height

    # Add edges to a new image
    imi = 
    pxi = im2.load() 
    
    # Convolute to a final image
    
    for x in range(width):
        for y in range(height):
            px[x,y] = 255 if px[x,y] < 128 else 0
    im.save("flipped-image.jpg")

    return print(form + " was successfully graded.  Output file '"+output_file+"' and '"+output_im+"' succcessfuly graded.")

################################################################################
# Run program
################################################################################

# Load command line inputs
form, output_im, output_file = sys.argv[1:]

# Grade form
# cProfile.run("grade(form, output_im, output_file)")
grade(form, output_im, output_file)