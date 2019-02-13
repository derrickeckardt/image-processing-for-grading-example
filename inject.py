#!/usr/bin/env python3
#
#   ./inject.py : Injecting encoded answers onto a blank answer sheet:
#     ./inject.py form.jpg answers.txt injected.jpg
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

def get_answers(answers_file):
    answers = {}
    with open(answers_file, 'r') as file:
        for line in file:
            question, truth = int(line.split()[0]), line.split()[1]
            answers[question] = {}
            for option in 'ABCDE':
                if option in truth:
                    answers[question][option] = True
                else:
                    answers[question][option] = False
    return answers

def print_barcode2(answers,px):
    #starting position
    x, y = 100,350
    white = 255
    bar_width = 15
    color = 0

    # for finding later in extract
    for i in range(-20,-10):
        for j in range(100):
            px[x+i,y+j] = color


    # encrypts by shifting the answers anywhere between 0 and 4 places to the right (eg, 1 would mean A goes B, B to C etc)
    encryption = '0132043412033042104211120231443244131113302332044423434220110201202323332414230320444'
    letters = {'0':'ABCDE', '1':'BCDEA', '2': 'CDEAB', '3': 'DEABC', '4':'EABCD'}

    header_color = 1
    # outputs header bar that can be used for positioning, and recognizing when a new
    # question begins, and should make it immune to most scaling issues

    for question, shift in zip(range(1,len(answers)+1), encryption):
        y = 350
        for i in range(bar_width):
            for j in range(bar_width):
                px[x+i,y+j] = color if header_color == 1 else white
        header_color = header_color * -1
        y=350 + bar_width
        
        for letter in letters[shift]:
            for i in range(bar_width):
                for j in range(bar_width):
                    px[x+i,y+j] = color if answers[question][letter] == True else white
            y += bar_width
        x += bar_width
        
def print_barcode(answers,px):
    # Will print a muti-colored barcode with each answer.  added color to imply
    # meaning, no actual meaning, just to throw students off
    color_options = [(255,0,0),(0,255,0),(0,0,255)] # rgb
    
    #starting position
    x, y = 100,350
    white = (255,255,255)
    options = list('ABCDE')
    bar_width = 3
    color = (0,0,0)

    # Add leading element so we know barcode begins
    # this spacer tells it to ignore the first 5 symbols it picks up.
    # unless you know this, the answers will not make sense
    # for each test, this could be unique
    front_spacer = 3 
    for space in range(front_spacer):
        # color = choice(color_options)
        for i in range(bar_width):
            for j in range(200):
                px[x+i,y+j] = color
        x += bar_width
    
    # encode answers
    for question in range(1,len(answers)+1):
        # color = choice(color_options)
        for letter in options:
            for i in range(bar_width):
                for j in range(200):
                    if answers[question][letter] == True:  
                        px[x+i,y+j] = color
                    else:
                        px[x+i,y+j] = white
            x += bar_width

    # end bar, similarily this could be unique
    rear_spacer = 2 
    for space in range(rear_spacer):
        # color = choice(color_options)
        for i in range(bar_width):
            for j in range(200):
                px[x+i,y+j] = color
        x += bar_width

def inject(form, answers_file, injected_im):
    # import answers
    answers = get_answers(answers_file)
    
    # import form
    im = Image.open(form).convert('RGB')
    # im = Image.open(form).convert('L')  # for print_barcode2
    px = im.load()
    width, height = im.width, im.height

    # print barcode
    print_barcode(answers,px)
    
    #output file
    im.save(injected_im)
    
    print("Barcode successfully injected into '"+injected_im+"'.  Happy Test Taking!")

    
################################################################################
# Run program
################################################################################

# Load command line inputs
form, answers_file, injected_im = sys.argv[1:]

# Inject form
# cProfile.run("inject(form, answers_file, injected_im)")
inject(form, answers_file, injected_im)