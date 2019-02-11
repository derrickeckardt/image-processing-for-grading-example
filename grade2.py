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
from operator import itemgetter
import profile
import cProfile


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
            
def rotate_angle(rp1,rp2,cp1,cp2):
    rp_ang = math.degrees(math.atan((rp2[1] - rp1[1])/(rp2[0] - rp1[0])))
    cp_ang = math.degrees(math.atan((cp2[1] - cp1[1])/(cp2[0] - cp1[0])))
    return rp_ang-cp_ang
    
def scale(rp1,rp2,cp1,cp2):
    area_cp = (cp2[1] - cp1[1])  * (cp2[0] - cp1[0])
    area_rp = (rp2[1] - rp1[1])  * (rp2[0] - rp1[0])
    return (area_cp / area_rp)**0.5    
    
def ref_points(px,width,height,location):
    # find the location of reference points
    # upper left postion, location = 0, or bottom right, location = -1
    # 255 used to make sure mreference points to accidently noise
    for y in range(height*(-1*location)+location,height+(location*height)+location,1+2*location): # length
        row_total = sum([px[x,y] for x in range(width)])
        if row_total > 255*5:
            break
    for z in range(width*(-1*location)+location,width+(location*width)+location,1+2*location): # width
        column_total = sum([px[z,x] for x in range(height*(-1*location)+location,int(height/2)+location,1+2*location)])
        if column_total > 255*5:
            break
    return z,y
    
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

    # Starken the difference, makes it easier to work with 0s instead of 255s
    stark_difference(px2,width,height)

    # find angle to rotate image
    # first, get reference points from blank_image.jpg. They coorspond to ideal
    # orientation They were found using the threshold function onblank_image.jpg
    # and then hard-coded, since not sure siystem we will be using
    # then,we look for the same points in the any scanned document.
    rp1 = (92,68)
    rp2 = (711,1039)
    
    # find reference points on original
    cp1 = ref_points(px2,width,height,0)
    cp2 = ref_points(px2,width,height,-1)

    # finally, rotate the image
    im3 = im2.rotate(rotate_angle(rp1,rp2,cp1,cp2))
    px3 = im3.load()
    
    # Now, scan for incidents
    # Since we know that boxes are 32 pixels wide by 32 pixels, we'll scan for
    # for boxes with the most lit up pixels
    # then eliminate the ones too close to others
    # then, sort by density, so we can determine the filled out onces
    # using a threshold of at least 40% are filled in
    # and then by location, to determine the location of them, and if there is
    #something to left of the number
    filled = int(16 * 16 * 0.25)
    filled_x = []
    filled_y = []

    range_16 = range(16)
    
    for x in range(width-16):
        for y in range(int(height/4), height-16):  # ignoring the first chunk of text
            box_total = sum([1 for i in range_16 for j in range_16 if px3[x+i,y+j] == 255])
            if box_total >= filled:
                # filled_y.append(([box_total,x,y]))   
                if len(filled_y) > 0:
                    if y-8 < filled_y[-1][2] and x-8 < filled_y[-1][1] :
                        if box_total > filled_y[-1][0]:
                            filled_y[-1] = [box_total,x,y]
                    else:
                        filled_y.append(([box_total,x,y]))   
                else:
                    filled_y.append(([box_total,x,y]))

    for y in range(int(height/4), height-16):  # ignoring the first chunk of text
        for x in range(width-16):
            box_total = sum([1 for i in range_16 for j in range_16 if px3[x+i,y+j] == 255])
            if box_total >= filled:
                if len(filled_x) > 0:
                    if y-8 < filled_x[-1][2] and x-8 < filled_x[-1][1] :
                        if box_total > filled_x[-1][0]:
                            filled_x[-1] = [box_total,x,y]
                    else:
                        filled_x.append(([box_total,x,y]))   
                else:
                    filled_x.append(([box_total,x,y]))

    # will check the x list and the y list, and it appears in both, I use it.
    combined_filled = []
    for each in filled_x:
        if each in filled_y:
            combined_filled.append(each)
    combined_filled = sorted(combined_filled, key=itemgetter(0,1), reverse = True)

    # get out overlaps, by taking the brightest one
    # i = 0
    sublist = []
    while len(combined_filled) > 0:
        each = combined_filled.pop(0)
        sublist_points = sorted([ point for point in combined_filled if (each[1]+16 > point[1] and each[2]+16 > point[2] and each[1]-16 < point[1] and each[2]-16 < point[2])] + [each], key=itemgetter(0), reverse=True)
        if sublist_points[0] not in sublist:
            sublist.append(sublist_points.pop(0))
            if len(sublist_points) > 0:
                for point in sublist_points:
                    if point in combined_filled:
                        combined_filled.remove(point)

    sublist = sorted(sublist, key=itemgetter(2,1))

    # determine which box the squares are in
    def box_check_total(point,multiple,px):
        x,y = point[1:3]
        x_spacer = 56 / 2
        box_total = sum([1 for i in range_16 for j in range_16 if px[x+i+x_spacer*multiple,y+j] == 255])
        return box_total

    # look for numbers of scratch marks written in margin as false positives
    finalist = []
    letters = [[1,"E"], [2, "D"], [3,"C"], [4,"B"], [5,"A"]]
    x_spacer = 56 / 2
    for j in range(len(sublist)):
        for i, letter in letters:
            if box_check_total(sublist[j],i,px3) == 0:
                if box_check_total(sublist[j],i-7,px3) >= 10:
                    finalist.append(sublist[j]+[letter,"x"])
                else:
                    finalist.append(sublist[j]+[letter,""])
                break

    print(len(finalist))
    
    #sort them to their questions, first find row number
    finalist1 = sorted(finalist, key=itemgetter(2,1))*1
    row_num = 0
    while len(finalist1) > 0:
        row_num += 1
        each = finalist1.pop(0)
        row_points = sorted([point+[row_num] for point in finalist1 if point[2] < each[2] + 16]+[each+[row_num]],key=itemgetter(1))
        for rowp in row_points:
            if rowp[0:-1] in finalist1:
                finalist1.remove(rowp[:-1])
            finalist[finalist.index(rowp[0:-1])].append(row_num)

    # then sort them to find column number
    finalist1 = sorted(finalist, key=itemgetter(3,1))*1
    col_num = 0
    while len(finalist1) > 0:
        each = finalist1.pop(0)
        col_points = sorted([point + [col_num] for point in finalist1 if point[1] < each[1] + 135]+[each+[col_num]],key=itemgetter(1))
        for colp in col_points:
            if colp[0:-1] in finalist1:
                finalist1.remove(colp[0:-1])
            finalist[finalist.index(colp[0:-1])].append(col_num)
        col_num += 1

    for i in range(len(finalist)):
        finalist[i].append(finalist[i][5] + finalist[i][6]*29)

    finalist = sorted(finalist, key=itemgetter(7,5))
    print(finalist)

    last_number = 0
    x_crossed = ""
    new_line = ""
    output_txt= open(output_file,"w+")
    for each in finalist:
        if last_number != 0:
            if each[7] > last_number:
                if x_crossed == "x":
                    output_txt.write(new_line+" x")
                else:
                    output_txt.write(new_line)
                x_crossed = ""
                if each[4] == "x":
                    x_cross = "x"    
                new_line = str(each[7])
    if x_crossed == "x":
        output_txt.write(new_line+" x")
    else:
        output_txt.write(new_line)
    output_txt.close
        

    # for i in range(len(rows)):
    #     row = rows.pop(0)
    #     for j in range(len(row)):
    #         final_dict[i+1] = {"value": point[3], "X" : point[4]}
            
        

    # temporary output
    for each in finalist:
        for x in range_16:
            for y in range_16:
                px3[each[1]+x,each[2]+y] = 128
        if each[4] == "x":
            for x in range(8):
                for y in range(8):
                    px3[each[1]+x,each[2]+y] = 192

            
    # Final output image
    im3.save(output_im)

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