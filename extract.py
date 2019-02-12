#!/usr/bin/env python3
#
# ./extract.py : Grading automated scanned answer sheet:
#     ./extract.py injected.jpg output.txt 
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

import sys
import PIL
import cProfile
from PIL import Image, ImageFilter
from pprint import pprint
from timeit import timeit
import math
from random import choice
from operator import itemgetter

def get_barcode(px, width):
    # assuming relatively the same placement starting to the left of where the 
    # middle should be
    x, y = 50,450

    front_spacer = 3
    rear_spacer = 2
    bar_width = 3

    for i in range(width-x):
        

    barcode = []
    return barcode
    
def decode(barcode):
    answers = {}
    return answers

def print_barcode(answers,px):
    # Will print a muti-colored barcode with each answer.  added color to imply
    # meaning, no actual meaning, just to throw students off
    color_options = [(255,0,0),(0,255,0),(0,0,255)] # rgb
    
    #starting position
    x, y = 100,350
    white = (255,255,255)
    options = list('ABCDE')
    bar_width = 3

    # Add leading element so we know barcode begins
    # this spacer tells it to ignore the first 5 symbols it picks up.
    # unless you know this, the answers will not make sense
    # for each test, this could be unique
    spacer = 3 
    for space in range(spacer):
        color = choice(color_options)
        for i in range(bar_width):
            for j in range(200):
                px[x+i,y+j] = color
        x += bar_width
    
    # encode answers
    for question in range(1,len(answers)+1):
        color = choice(color_options)
        for letter in options:
            for i in range(bar_width):
                for j in range(200):
                    if answers[question][letter] == True:  
                        px[x+i,y+j] = color
                    else:
                        px[x+i,y+j] = white
            x += bar_width

    # end bar, similarily this could be unique
    spacer = 2 
    for space in range(spacer):
        color = choice(color_options)
        for i in range(bar_width):
            for j in range(200):
                px[x+i,y+j] = color
        x += bar_width
        
    print(x)

def ref_points(px,width,height,location):
    # find the location of reference points
    # upper left postion, location = 0, or bottom right, location = -1
    # 255 used to make sure mreference points to accidently noise
    # modifieid from grade.py
    for y in range(height*(-1*location)+location,height+(location*height)+location,1+2*location): # length
        row_total = sum([1 for x in range(width) if px[x,y] < 255])
        if row_total > 5:
            break
    for z in range(width*(-1*location)+location,width+(location*width)+location,1+2*location): # width
        column_total = sum([1 for x in range(0,250) if px[z,x] < 255])
        if column_total > 5:
            break
    return z,y

def rotate_angle(rp1,rp2,cp1,cp2):
    rp_ang = math.degrees(math.atan((rp2[1] - rp1[1])/(rp2[0] - rp1[0])))
    cp_ang = math.degrees(math.atan((cp2[1] - cp1[1])/(cp2[0] - cp1[0])))
    return rp_ang-cp_ang

def extract(injected_im, output_txt):
    # import injected form
    im = Image.open(injected_im).convert('L')
    px = im.load()
    width, height = im.width, im.height

    # ensure form hasn't rotate, if it has, rotate it.  New reference points
    rp1 = (0,0)
    rp2 = (180,136)

    # find reference points on original
    cp1 = (0,0)
    cp2 = ref_points(px,width,height,0)
    print(cp1,cp2)

    # finally, rotate the image
    angle_to_rotate = rotate_angle(rp1,rp2,cp1,cp2)
    im2 = im.rotate(angle_to_rotate)
    px2 = im2.load()

    # get barcode
    barcode = get_barcode(px2, width)

    # import answers
    answers = decode(barcode)

    print("Answers successfully extracted from '"+injected_im+"' and outputted into '"+output_txt+"'. Happy Grading!")
    
################################################################################
# Run program
################################################################################

# Load command line inputs
injected_im, output_txt = sys.argv[1:]

# Inject form
# cProfile.run("extract(injected_im, output_txt)")
extract(injected_im, output_txt)