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

def add_edges_dict(im,filter_matrix):
    im_px = im.load()
    im_width = im.width
    im_height = im.height
    fm_size = [len(filter_matrix), len(filter_matrix[0])]
    row_edges = int(fm_size[1]/2)
    col_edges = int(fm_size[0]/2)
    edged_im = Image.new("L", (im_width + 2*row_edges, im_height + 2*col_edges), color = 255)
    edged_im_px = edged_im.load()
    # copy image over and add blank edges
    for i in range(im_width):
        for j in range(im_height):
            edged_im_px[i+row_edges,j+col_edges] = im_px[i,j]#im.getpixel((i,j)))
    # add left and right edges first
    edged_im_px = edged_im.load()
    for j in range(edged_im.height):
        for i in range(row_edges):
            edged_im_px[i,j] =edged_im_px[row_edges,j]
            edged_im_px[i+im.width+row_edges,j] = edged_im_px[im.width+row_edges-1,j]
    # add top and bottom edges, which copy the adjacent edge
    edged_im_px = edged_im.load()
    for i in range(edged_im.width):
        for j in range(col_edges):
            edged_im_px[i,j] = edged_im_px[i,col_edges]
            edged_im_px[i,im.height+col_edges+j]= edged_im_px[i,im.height+col_edges-1]
    return edged_im

def convolute3(im,filter_matrix):
    edged_im = add_edges_dict(im,filter_matrix)
    edged_im_px = edged_im.load()
    convol_row, convol_col = len(filter_matrix), len(filter_matrix[0])
    row_edges = int(convol_row/2)
    col_edges = int(convol_col/2)
    im_width = im.width
    im_height = im.height
    output_im = Image.new("L", (im_width, im_height), color = 0)
    output_im_px = output_im.load()
    for i in range(im_width):
        for j in range(im_height):
            convol_total = 0
            for x in range(convol_row):
                for y in range(convol_col):
                    convol_total += filter_matrix[x][y] * edged_im_px[i+x,j+y]
            output_im_px[i,j] = int(convol_total)

    return output_im

def binary_image_filter(im, px):
    im_width = im.width
    im_height = im.height
    instance = Counter()
    instance_pre = Counter()
    for x in range(im_width):
        for y in range(im_height):
            instance_pre[px[x,y]] += 1
            px[x,y] = 255 if px[x,y] < 128 else 0
            instance[px[x,y]] += 1
    print(instance_pre)
    print(instance)
    return im, px

def find_angle(px):
    for i in range(10):
        print("ADD THE FIND ANGLE MODULE!")
    return px
    
def simplify_image(im,px):
    # filter intensities
    im, px = binary_image_filter(im,px)

    # filter with box blur to reduce noise
    box_blur_matrix_dict = {}
    for x in range(3):
        box_blur_matrix_dict[x] = {}
        for y in range(3):
            box_blur_matrix_dict[x][y] = 1.0/9.0
    im = convolute3(im,box_blur_matrix_dict)
    px = im.load()

    # filter intensities again, to further get rid of noise
    im, px = binary_image_filter(im,px)

    return im, px

def grade(form, output_im, output_file):
    print("Recognizing "+form+"...")
    # resizing image, importing as grayscale
    im = Image.open(form).convert('L').resize((850,1100))
    px = im.load()

    # find angle of rotation
    angle = find_angle(im,px)

    # clear out noise and simplify image
    im, px = simplify_image(im,px)

    im.save('resized_img.jpg')
    
def output(output_file):
    print("Outputting to "+output_file)
    print("Output completed.")
    
################################################################################
# Run program
################################################################################

# Load command line inputs
form, output_im, output_file = sys.argv[1:]

# Grade form
# cProfile.run("grade(form, output_im, output_file)")
grade(form, output_im, output_file)