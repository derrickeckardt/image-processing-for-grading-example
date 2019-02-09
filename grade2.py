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


def add_edges_dict(px,filter_matrix, width, height):
    im_width = width
    im_height = height
    fm_size = [len(filter_matrix), len(filter_matrix[0])]
    row_edges = int(fm_size[1]/2)
    col_edges = int(fm_size[0]/2)
    edged_im = Image.new("L", (im_width + 2*row_edges, im_height + 2*col_edges), color = 255)
    edged_im_px = edged_im.load()
    # copy image over and add blank edges
    for i in range(im_width):
        for j in range(im_height):
            edged_im_px[i+row_edges,j+col_edges] = px[i,j]#im.getpixel((i,j)))
    # add left and right edges first
    edged_im_px = edged_im.load()
    for j in range(edged_im.height):
        for i in range(row_edges):
            edged_im_px[i,j] =edged_im_px[row_edges,j]
            edged_im_px[i+im_width+row_edges,j] = edged_im_px[im_width+row_edges-1,j]
    # add top and bottom edges, which copy the adjacent edge
    edged_im_px = edged_im.load()
    for i in range(edged_im.width):
        for j in range(col_edges):
            edged_im_px[i,j] = edged_im_px[i,col_edges]
            edged_im_px[i,im_height+col_edges+j]= edged_im_px[i,im_height+col_edges-1]
    return edged_im

def convolute(px,filter_matrix, width,height):
    convol_row, convol_col = len(filter_matrix), len(filter_matrix[0])
    row_edges = int(convol_row/2)
    col_edges = int(convol_col/2)
    im_width = width
    im_height = height
    output_im = Image.new("L", (im_width, im_height), color = 0)
    output_im_px = output_im.load()
    for i in range(im_width):
        for j in range(im_height):
            convol_total = 0
            for x in range(convol_row):
                for y in range(convol_col):
                    convol_total += filter_matrix[x][y] * px[i+x,j+y]
            output_im_px[i,j] = int(convol_total)
    return output_im
    
def stark_difference(px_load, width, height):
    for x in range(width):
        for y in range(height):
            px_load[x,y] = 255 if px_load[x,y] < 160 else 0
    
def grade(form, output_im, output_file):
    print("Importing "+form+"...")
    # Set-up
    im = Image.open(form).convert('L').resize((850,1100))
    px = im.load()
    width = im.width
    height = im.height
    
    # box blur filter matrix
    box_blur = {}
    for x in range(3):
        box_blur[x] = {}
        for y in range(3):
            box_blur[x][y] = 1.0/9.0

    # Add edges to a new image
    im1 = add_edges_dict(px,box_blur,width,height)
    px1 = im1.load() 

    # Convolute to a final image
    im2 = convolute(px1,box_blur,width,height)
    px2 = im2.load()

    # Starken the difference
    stark_difference(px2,width,height)

    # find angle to rotate image
    for y in range(1099,1000,-1): # length
        row_total = sum([px2[x,y] for x in range(width)])
        if row_total > 0:
            print(x,y)
            break
        
            

    # Final output image
    im2.save(output_im)

    print("Hooray! "+form + " was successfully graded.")
    print("Output files '"+output_file+"' and '"+output_im+"' succcessfuly graded.")

################################################################################
# Run program
################################################################################

# Load command line inputs
form, output_im, output_file = sys.argv[1:]

# Grade form
# cProfile.run("grade(form, output_im, output_file)")
grade(form, output_im, output_file)