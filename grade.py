#!/usr/bin/python3
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
import profile
from PIL import Image
from collections import Counter
from pprint import pprint
import numpy as np
from timeit import timeit

def add_edges(im,filter_matrix):
    im_px = im.load()
    fm_size = filter_matrix.shape
    row_edges = int(fm_size[1]/2)
    col_edges = int(fm_size[0]/2)
    edged_im = Image.new("RGB", (im.width + 2*row_edges, im.height + 2*col_edges), color = (0,0,0))
    # copy image over and add blank edges
    for i in range(im.width):
        for j in range(im.height):
            edged_im.putpixel((i+row_edges,j+col_edges),im_px[i,j])#im.getpixel((i,j)))
    # add left and right edges first
    edged_im_px = edged_im.load()
    for j in range(edged_im.height):
        for i in range(row_edges):
            edged_im.putpixel((i,j),edged_im_px[row_edges,j])
            edged_im.putpixel((i+im.width+row_edges,j),edged_im_px[im.width+row_edges-1,j])
    # add top and bottom edges, which copy the adjacent edge
    edged_im_px = edged_im.load()
    for i in range(edged_im.width):
        for j in range(col_edges):
            edged_im.putpixel((i,j),edged_im_px[i,col_edges])
            edged_im.putpixel((i,im.height+col_edges+j),edged_im_px[i,im.height+col_edges-1])
    return edged_im

def convolute2(im,im_px, filter_matrix):
    # flip matrix
    filter_matrix = np.fliplr(np.flipud(filter_matrix)) 
    edged_im = add_edges(im,filter_matrix)
    edged_im_px = edged_im.load()
    convol_row, convol_col = filter_matrix.shape
    row_edges = int(convol_row/2)
    col_edges = int(convol_col/2)
    output_im = Image.new("L", (im.width, im.height), color = 0)
    for i in range(im.width):
        for j in range(im.height):
            convol_total = np.array([0]*3)
            for x in range(convol_row):
                for y in range(convol_col):
                    interim_1 = filter_matrix[x][y]
                    interim_2 = edged_im_px[i+x,j+y]
                    interim = np.multiply(interim_1,interim_2)
                    convol_total = interim + convol_total
            output_im.putpixel((i,j),int(convol_total[0]))

    return output_im

def binary_image_filter(im, px):
    for x in range(im.width):
        for y in range(im.height):
            px[x,y] = 0 if px[x,y] < 128 else 255



def grade(form, output_im, output_file):
    print("Recognizing "+form+"...")
    # resizing image
    # importing as grayscale
    im = Image.open(form).convert('L').resize((850,1100))
    px = im.load()


    # filter intensities
   # binary_image_filter(im,px)

    # filter with gaussian to get rid of noise
    box_blur_matrix = 1/9 * np.array([[1.0]*3]*3)

    # c - gaussian
    gaussian_matrix = np.array([[0.003, 0.013, 0.022, 0.013, 0.003],
                                [0.013, 0.059, 0.097, 0.059, 0.013],
                                [0.022, 0.097, 0.159, 0.097, 0.022],
                                [0.013, 0.059, 0.097, 0.059, 0.013],
                                [0.003, 0.013, 0.022, 0.013, 0.003]])
    im = convolute2(im,px,box_blur_matrix)
    px = im.load()


    # filter intensities again, to get rid of noise
    binary_image_filter(im,px)

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
#profile.run("grade(form, output_im, output_file)")
grade(form, output_im, output_file)