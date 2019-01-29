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

def grade(form, output_im, output_file):
    print("Recognizing "+form+"...")
    im = Image.open(form).convert('L')
    print(im.getpixel((200,200)))
    print(im.size)  # 1700x2200
    #resize image to simplify calculation
    
    
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