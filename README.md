# a1

# Grading program

## Importing the image
When key decision I made was to important the image as grayscale.

## Resizing the image.
The images were 1700 x 2200 pixels.  Those are fairly large.  So, I played around with some reduced images sizes that I felt did not lose fidelity.  The benefit is that a smaller image would be computationally less intensive.  By reducing length and width by 50% each, makes my image only a fourth as large.  Higher values might be possible.

As a check, i did run itat 100% and got the same results.
# FIX ME LATER

## Filtering the images
At the beginning, I decided to look at the intensities of the ink, and on the sample images, I found that almost all the pixels were within 20 of either 0 or 255 intensity-level, indicating that the pixels were all basically white or black.  For example, here is the distribution of intensities for test images a3.jpg:

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

Because of that, I ran a quick filter to change them all to 0 or 255, where I split them at 128.  This could potentially introduce some error for someone who did not fill them in very full.  Even for test-image a-48, which had some very light markings, splitting down the middle was still a good measure.