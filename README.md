# CS B657 - Assignment 1: Image Processing and Recognition Basics

Completed by Derrick Eckardt on February 12, 2019.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 1 Prompt](https://github.iu.edu/cs-b657-sp2019/derrick-a1/blob/master/a1.pdf)

# Grading program - grade.py

## The Problem
First, the problem is presented with a answer sheet for a test.  It's a typical looking bubblesheet, with 85 questions.  The goal is to write a program that can read the answers filled out the by the student, determine if they put relevant markings in the margins, and then output this into two documents.  The first one is a text file that gives the letters and markings for each question, in a format specified in the prompt.  The second document is a copy of the student's completed answer sheet that has been annotated with the answers and margin markings the grade.py program found.

## Importing the image
To begin, a key decision I made was to important the image as grayscale.  This makes the numbers easier to work with, and later makes it easier to highlight.  I tried early on with RGB color, but that created issues in determing the important of what was in a pixel that weren't worth the hassle.

## Resizing the image.
The images were 1700 x 2200 pixels.  Those are fairly large to look at pixel by pixel.  So, I played around with some reduced images sizes that I felt did not lose fidelity.  The benefit is that a smaller image would be computationally less intensive.  By reducing length and width by 50% each, makes my image only a fourth as large, and four times faster to evaluate.  THere is probably some ideal value that might be lower that allows for even faster processing, but it was not worth the time to optimize that further for diminishing returns, since I had already cut processing time down 75% by using a 50% reduction.

## Filtering the images
Since the images had first been printed, and then scanned, there was some noise that was created as a result of two machines and several humans touching the documents.  To handle that I took a two-part approach.  First, I would do some box filtering, and then make the colors binary -- white or black.

### Box Filtering the Images
Because of the noise, I wanted to get rid of as much of it as I could.  The first part of that began with running a simple box filter over it.  The rationale was that if there was an errant pixel, it would easily then get smoothed out when I made the difference much starker.

### Starkening the Difference
Next, I took a look at the intensities of the ink, and on the sample images, I found that almost all the pixels were within 40 of either 0 or 255 intensity-level, indicating that the pixels were all basically white or black.  For example, here is the distribution of intensities for test images a3.jpg:

```
{0: 125972,
 1: 30101,
 2: 18783,
 3: 15247,
 4: 11844,
 5: 8724,
 6: 5859,
 7: 3935,
 8: 2371,
 9: 1460,
 10: 744,
 11: 429,
 12: 213,
 13: 85,
 14: 34,
 15: 16,
 16: 3,
 17: 4,
 18: 1,
 236: 1,
 237: 2,
 238: 3,
 239: 10,
 240: 34,
 241: 147,
 242: 244,
 243: 506,
 244: 1208,
 245: 2455,
 246: 4132,
 247: 6942,
 248: 11665,
 249: 16356,
 250: 22534,
 251: 33716,
 252: 42046,
 253: 56994,
 254: 89774,
 255: 3225406}
 ```

Because of that, I ran a quick filter to change them all to 0 or 255, where I split them at 160.  This could potentially introduce some error for someone who did not fill them in very full.  Even for test-image a-48, which had some very light markings, this split was still a very good measure.  The other benefit to this is that it made the filled in parts equal to 255 and the empty spots 0, which are easier to do calculations with later on.

### Comments about filtering
A concern I had during this time was that this filtering would get rid of many of the markings that had gone into the margins of the sheet, which students are instructed to do if they made a mistake.  A visual inspection of the sheets showed that for some it did increase the difficulty.  However, it did not seem out of reach.

## Rotating the Image
One thing I noticed is that the completed answer sheets often were slightly askew as a result of the printing and/or scanning of the answer sheets.  Since, it would be helpful for consistent results for the sheet to be consisently orientated.  To adjust for the rotation, I picked two reference points on the provided blank_form.jpg file, and then created a small function to find those two points, and then calculate the difference in rotation.  Then, I rotated my image.  Also, when Pillow rotates an image, it adds blank pixels where there was nothing.  Since, I had already reversed the colors in my starkening, that did not become an issue.



























