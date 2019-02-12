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
from collections import Counter
from random import choice
from operator import itemgetter

def decode_barcode(px, width):
    # assuming relatively the same placement starting to the left of where the 
    # middle should be
    
    #I take it in five difference places so that I can vote, to help reduce
    # the impact of noise
    x, y_range = 50, range(430,480,10)

    front_spacer = 3
    rear_spacer = 2
    bar_width = 3

    barcode = {}
    for y in y_range:
        barcode[y] = {}
        #find front pixels
        for i in range(x,width-x):
            probe_total = sum([1 for z in range(i,i+front_spacer*bar_width) if px[z,y] < 255])
            if probe_total == front_spacer*bar_width:
                break
        front = i
        #find rear pixels
        for i in range(width-x-1,-1,-1):
            probe_total = sum([1 for z in range(i,i-rear_spacer*bar_width,-1) if px[z,y] < 255])
            if probe_total == rear_spacer*bar_width:
                break
            pass
        back = i +1
    
        counter = 1
        for z in range(front+front_spacer*bar_width,back-rear_spacer*bar_width, bar_width):
            barcode[y][counter] = sum([px[z+i,y] for i in range(bar_width)])
            counter += 1

    answers = {}
    for i in range(1,426,5):
        answers[int(i/5)+1] = {}
        for j, letter in zip(range(5),'ABCDE'):
            votes = []
            for y in y_range:
                votes.append(barcode[y][i+j])
            result = Counter(votes)
            answers[int(i/5)+1][letter] = True if result.most_common(1)[0][0] <= 255*2 else False
    
    return answers

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

def stark_difference(px_load, width, height):
    for x in range(width):
        for y in range(height):
            px_load[x,y] = 0 if px_load[x,y] < 160 else 255

def scale(rp1,rp2,cp1,cp2):
    area_cp = (cp2[1] - cp1[1])  * (cp2[0] - cp1[0])
    area_rp = (rp2[1] - rp1[1])  * (rp2[0] - rp1[0])
    return (area_cp / area_rp)**0.5

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

    # assumption to note, these are assuming that the scan is at 100%.
    # I found that the scans were mostly all 96% of the given size, so image
    # will have to be scaled up in order to be the correct size

    # untested, lack of testing materials
    # scale_ratio = scale(rp1,rp2,cp1,cp2)

    # imshrink = im.resize((1632,2112), box=(34,44,1666,2156))
    # imshrink.save("imshrink.jpg")

    # x_scale_marg = int(width * (1.0-scale_ratio) / 2)
    # y_scale_marg = int(height * (1.0-scale_ratio) / 2)

    # # zooms into the relevant portion
    # im1 = im.resize((width,height),box=(x_scale_marg,y_scale_marg,width - x_scale_marg,height - y_scale_marg))
    # im1.save('rescaled.jpg')

    # finally, rotate the image
    angle_to_rotate = rotate_angle(rp1,rp2,cp1,cp2)
    im2 = im.rotate(angle_to_rotate)
    px2 = im2.load()

    
    # filter out any noise introduced reimporting it.
    stark_difference(px2,width,height)

    # get barcode and decode it
    answers = decode_barcode(px2, width)
    
    output_file= open("test-"+output_txt,"w+")
    for i in range(1,86):
        new_line = str(i)+" "
        for letter in 'ABCDE':
            if answers[i][letter] == True:
                new_line += letter
        output_file.write(new_line+"\n")
    output_file.close

    print("Answers successfully extracted from '"+injected_im+"' and outputted into '"+output_txt+"'. Happy Grading!")
    
################################################################################
# Run program
################################################################################

# Load command line inputs
injected_im, output_txt = sys.argv[1:]

# Inject form
# cProfile.run("extract(injected_im, output_txt)")
extract(injected_im, output_txt)