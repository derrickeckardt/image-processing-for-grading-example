# CS B657 - Assignment 1: Image Processing and Recognition Basics

Completed by Derrick Eckardt on February 12, 2019.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 1 Prompt](https://github.iu.edu/cs-b657-sp2019/derrick-a1/blob/master/a1.pdf)

# General Comments
All I could think about this was the many different ways students could break a well designed system.  Overall, I am really happy with how grade.py turned out.  I think I could spend weeks more on inject/extractin order to get a system that could get read despite being printed and scanned twice, which is surely going to mess with the values.  I am really happy with the 99.3% accurancy I got on grade.py (spoiler alert!).  I also think there are plenty of ways to improve all of these files, and also provide some recommendations on how inject and extract should be done with a different approach that reduces a lot of the issues I found with the request implementation.

# Grading program - grade.py - The Problem
First, the problem is presented with a answer sheet for a test.  It's a typical looking bubblesheet, with 85 questions.  The goal is to write a program that can read the answers filled out the by the student, determine if they put relevant markings in the margins, and then output this into two documents.  The first one is a text file that gives the letters and markings for each question, in a format specified in the prompt.  The second document is a copy of the student's completed answer sheet that has been annotated with the answers and margin markings the grade.py program found.

## Prepwork
Getting the image ready for analysis required several steps.

### Importing the image
To begin, a key decision I made was to important the image as grayscale.  This makes the numbers easier to work with, and later makes it easier to highlight.  I tried early on with RGB color, but that created issues in determing the important of what was in a pixel that weren't worth the hassle.

### Resizing the image.
The images were 1700 x 2200 pixels.  Those are fairly large to look at pixel by pixel.  So, I played around with some reduced images sizes that I felt did not lose fidelity.  The benefit is that a smaller image would be computationally less intensive.  By reducing length and width by 50% each, makes my image only a fourth as large, and four times faster to evaluate.  THere is probably some ideal value that might be lower that allows for even faster processing, but it was not worth the time to optimize that further for diminishing returns, since I had already cut processing time down 75% by using a 50% reduction.

### Filtering the images
Since the images had first been printed, and then scanned, there was some noise that was created as a result of two machines and several humans touching the documents.  To handle that I took a two-part approach.  First, I would do some box filtering, and then make the colors binary -- white or black.

#### Box Filtering the Images
Because of the noise, I wanted to get rid of as much of it as I could.  The first part of that began with running a simple box filter over it.  The rationale was that if there was an errant pixel, it would easily then get smoothed out when I made the difference much starker.  I had tried to use a gaussian, but that actually made it worse as it kept

#### Starkening the Difference
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

#### Comments about filtering
A concern I had during this time was that this filtering would get rid of many of the markings that had gone into the margins of the sheet, which students are instructed to do if they made a mistake.  A visual inspection of the sheets showed that for some it did increase the difficulty.  However, it did not seem out of reach.

### Rotating the Image
One thing I noticed is that the completed answer sheets often were slightly askew as a result of the printing and/or scanning of the answer sheets.  Since, it would be helpful for consistent results for the sheet to be consisently orientated.  To adjust for the rotation, I picked two reference points on the provided blank_form.jpg file, and then created a small function to find those two points, and then calculate the difference in rotation.  Then, I rotated my image.  Also, when Pillow rotates an image, it adds blank pixels where there was nothing.  Since, I had already reversed the colors in my starkening, that did not become an issue.

## Analysis - General Approach
Early on, we learned about the filters that are used for facial recognition.  They are very basic filters that went pixel by pixel looking for regions in images that different than other regions, such as darker near eyes than the surrounding area, it might be indicative of a face.  With multiple of those simple filters lopped on, it can find faces with surprising high accuracy.  Similarily, I thought such a filter would work well here, that if a box, the size of the bubble box had enough pixels completed, it was likely something of note.  Since all of the pixels had gone through the filtering, only the strongest of pixels remained.  Even, much of the bubble boxes got filtered away, so they did not create much noise.

### Filters are Simple and Work
So, I created a 16x16 filter box (remember,I scaled it down 50% in each axis) that counted pixels.  If 29% of the pixels were colored in, I said it was interesting.  First, my box went horizontally across, one pixel at a time and then vertically down.  Then, I did it vertically down and then horizontally across.  I also had it take the local best (within 8 pixels) since adjacent pixels would likely have similar values.  In each case, for a sample case, I got around 2500 vertically and then 2500 horizontally.  Then, I found the intersection of the two, which got me to about 300 points. With each sheet having about 110 bubbles completed, I was close, but not close enough. I then, once again had the points filtered to find points that overlapped.  Prior, I had only filtered out repeats within 8 pixels to err on the side of conservatism.  This approach worked out well, as I now had the appropriate amount of datapoints.

### What's an adequate threshold?
How did I get 29%?  That was through trial and error.  I created groundtruth files for all of the images.  I calculated which values for the threshold produced what kind of errors and how many total errors.  I used it to troubleshoot and fix some of those errors.  I found at a threshold between 29% and 30%, as many errors as possible were minimized.  I went with 29% since at 31% some errors were caused by students filling it in too lightly.  At lower than 28%, the blank boxes themselves started to show up, particularly the Bs, because Bs already have a lot of pixels.  This number is definitely tuned, and I got different errors on different sheets dependings on threshold.

### Using White Space to Find the Letters
After getting my final set of points, I used the distance to the white space on the right as a relative guide to determine if points represented A, B, C, D, or E.  Then, with a similar method, I looked for any sort of markups on the space of the left to indicate something of note might be there for an instructor to see.

### More sorting
Now, I had all of points assigned to letters and they carried with the information that might be something in the margin.  But, I didn't know to which question they belonged to.  In order to determine the locations of the points, I first sorted them vertically and assigned them to a row, and then horizontally and assigned them to a column.  I used the known width of a row and column to aid in the sorting process.  Once, I had the row and column, I calculated the question number.

Finally, with the question numbers, letter, and margin markings, I was able to create the output.txt file.

Creating the output.img file was straight forward, as I draw a box, with my known points representing the upper corner.  I was also able to draw boxes around the white space where things had been marked.

### (Not) Understanding the Student's Intent
This question came up when looking at test image A48, Question 64, letter A, and on C33, Question 82, letter A.  The first one (A48) the box is filled in about one-third.  The second one (C33) it appears the pen might have been pushed down on the box, and either erased or not completely filled.  Other boxes in the area show that the student tended to have really strong pen marks, indicating where they began coloring in the box.  Or, did I imagine it in both these cases.  THis is the challenge for computer vision, we're trying to ask a machine to interrupt what might not be straight forward for a human to determine. I tended to favor, if there is a mark, then it counts, since I cannot begin to guess someone's intent.

## Results
Amazingly to my own surprise, my program was able to correctly identify 675 of 680 questions for a 99.3% accuracy.  The errant solutions were a result of probably noise, or perhaps residue from eraser marks that was dark enough to show up on the image.  Overall, I am happy with the results, but there are many

## Recommendations for Improvement of Grade.py

### Recognize the Oddities
The most amazing thing about business is that when you give someone a product, they will find ways to use it that you could never have imagined or anticipated.  The best improvement for this is program would be for it to identify when a student does something that is non-standard.  Perhaps they doodled in the margin, or wrote an extensive note to the instructor on it.  SOmething like that will likely break the best of systems unless they are anticipated for.  And even then, it still mgiht break.  Perhaps a neural network that focuses on everything outside of the boxes, while we only were really focused on the boxes and the spaces just outside of them, might be able to flag for instructors that a particular sheet should be looked at.

### Voting method
To get the absolute best results, multiple techniques should be deployed, and then using a system vote to determing which are the final answers, or at a minimum, to flag the ones that a human might need to check out for the final word.  Now that the instructors have 50 different approaches, they could take the ten best, and see what a consolidated result looks like.

### Refactoring the Code
This code takes less than one minute to run scoresheet.  I think with a better data structure, and more efficiently looping, incorporation of dyanmic programming, and other techniques, it could run much faster.  A faster running program allows fewer resources to be used and/or multiple techniques to be tried during a 'reasonable' amount of time.

### Adding a line to the instructions
With that previous point and the earlier discussion about student intent, the instructions should be updated to indicate that "any marks" might result in incorrect grading, so students should be careful with their pens.  I might go as far as banning erasing, and requiring the notes in the margin, since those can be picked up fairly easily.

# Answer Injecting and Extracting- Inject.py and Extract.py - The Problem
Here, we were tasked with injecting some sort of encoding that allowed

# Attempt 1 -  1D Barcode
This is a rather straightforward approach.  I went from 1 to 85, left to right, and a through A.  If the value was True, it printed in black, if not, it printed in white.  There were spacer bars added to throw off where it began.

## Extracting the measures
Then, when extract.py ran, it looked for the beginning, went past the spacer bars, and then started counting what it found at each three pixels.  To account for noise, I took samples at 5 difference cross-sections of the bar code

## Security measures
This is pretty low on the security, but effective.  The bar code is not a natural thing to look at it.  Plus, I added leading and trailing bars of different lengths that could confuse the student, if s/he was attempting to decode while taking the test.  The bars are only 3 pixels wide. Even a program that didn't know it, wouldn't necessarily figure it out without

One low-fidelty security measure I attempted was having it generate the bars in random red,blue, or green.  The thought would be it would make the barcode look that much harder, and it added implied meaning, but no actual meaning.  You can see this as an artificat in the code that the document is encoded in RGB instead of black and white.

# Attempt 2 - 2D Barcode with Encryption
While looking for a better way to do Attempt 1, I realized I could do a much cleaner version if I went into two-dimensions.  This is more akin to a QR code.   I put a spacer bar on the left, and dots on the top for orientation.

    This is currently deactivated.  If you would like to see this one, in inject.py change line 132 to convert to L instead of RGB (as is written in the comment on line 133), and then change line 138 to print_barcode2.  Similar change has to be made in extract.py

To determine whether a square was checked, I attempted to locate the center of the square, and then vote with the 9 center most pixels.  This was done to account for any noise that might have flipped the pixels. I ran into problems with this one because it also did not like scaling.

Given the two options I had working, I went the barcode, as it seemed to work the best overall.

## Security measures
Since, I was essentially setting up a 2-D grid of the answers, some sort of security would be needed.  Since there were 85 questions, i created a string of 85 numbers ranging from 0 to 4, which would indicate how many the actual values would be rotated.  It would also be a bit taunting showing the answers are there, just scrambled a bit.

## Results
It works.  Both of them.  However, the thing that is the most concern to me is what happens when it gets printed and then rescanned.  A 1% in reduction in size, means 17 fewer pixels, which need to come from somewhere in our barcodes.

## Recommendations
Here are some thoughts I had on how to make this better.

### Why Are We Overcomplicating it?
Rather than encoding the answers and then extracting them, which could introduce for the reasons I've pointed out, why not just print, in large, noise-absorbing letter a 6-digit serial number.  Since as we learned that OCR is well developed for things like digits and letters, this would be rather straightforward (and something we did last semester in B551).  Then, the serial number would correspond to the answer set, which would reside on the instructor's computer.  That answer set would have already been generated when the student's test was generated.  This way we make it really easy to outmate the answer key for a particular test, but we don't have to worry about things like noise and scale reductions caused by scanning and printing.

### Better algorith
Rather than dealing with absolute values, I would come up with something that crawled my bar code, looking for differences, and if things shrank or were widened, it wouldn't matter, because only the differences would matter.  Overall, not really happy with how it came out, there is definitely room for improvement on the injecting algorithm in order to facilitate better extraction.

### Find Better Way to Deal with Scale
Overall, I was very unhappy with the methods that I came up with the variablity in scale that would likely happy.