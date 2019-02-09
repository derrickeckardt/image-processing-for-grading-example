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
import math


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
            
def rotate_angle(px,width, height):
    scale = 0
    return scale
    
def grade(form, output_im, output_file):
    print("Importing "+form+"...")
    # Set-up
    im = Image.open(form).convert('L').resize((850,1100))
    px = im.load()
    width, height = im.width, im.height

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
    # use 255*5 as a threshold to allow for a little bit of noise
    
    # These reference point are from blank_image.jpg. Tthey coorspond to ideal orientation
    # They were found using the algorithm below, and was then used to determine
    # the orientation of any scanned document
    rp1 = (92,68)
    rp2 = (711,1039)
    
    area_rp = (rp2[1] - rp1[1])  * (rp2[0] - rp1[0])

    def threshold(px,width,height,location):
        print(height*(-1*location)+location,height+(location*height)+location,1+2*location)
        for y in range(height*(-1*location)+location,height+(location*height)+location,1+2*location): # length
            row_total = sum([px[x,y] for x in range(width)])
            if row_total > 255*5:
                break
        print(width*(-1*location)+location,width+(location*width)+location,1+2*location)
        print("x-range: ",height*(-1*location)+location,int(height/2)+location,1+2*location)
        for z in range(width*(-1*location)+location,width+(location*width)+location,1+2*location): # width
            column_total = sum([px[z,x] for x in range(height*(-1*location)+location,int(height/2)+location,1+2*location)])
            if column_total > 255*5:
                break
        return z,y
        
    
    # find reference point 1
    for y in range(0,height): # length
        row_total = sum([px2[x,y] for x in range(width)])
        if row_total > 255*5:
            break
    for z in range(0,width):
        column_total = sum([px2[z,x] for x in range(0,400)])
        if column_total > 255*5:
            break
    cp1 = (z,y)
    cp1_alt = threshold(px2,width,height,0)
    cp2_alt = threshold(px2,width,height,-1)

    
    print("Refer 1 Point:",rp1[0],rp1[1])
    print("Current Point:",cp1[0],cp1[1])
    print("Current Point_alt:",cp1_alt)

    # find reference point 2
    for y in range(height-1,-1,-1): # length
        row_total = sum([px2[x,y] for x in range(width)])
        if row_total > 255*5:
            break
    for z in range(width-1,-1,-1):
        column_total = sum([px2[z,x] for x in range(height-1,height-401,-1)])
        if column_total > 255*5:
            break
        
    cp2 = (z,y)

    area_cp = (cp2[1] - cp1[1])  * (cp2[0] - cp1[0])

    print("Refer 2 Point:",rp2[0],rp2[1])
    print("Current Point:",z,y)
    print("Current Point_alt:",cp2_alt)


    print("Area RP:", area_rp)
    print("Area CP:", area_cp)

    print(area_cp / area_rp)
    scale = (area_cp / area_rp)**0.5
    print(scale)
    
    rp_ang = math.degrees(math.atan((rp2[1] - rp1[1])/(rp2[0] - rp1[0])))
    cp_ang = math.degrees(math.atan((cp2[1] - cp1[1])/(cp2[0] - cp1[0])))
    print(rp_ang, cp_ang)

    im3 = im2.rotate(rp_ang-cp_ang) 
            
    # Final output image
    im3.save("r-"+output_im)

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