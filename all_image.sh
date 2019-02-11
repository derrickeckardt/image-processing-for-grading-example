#!/bin/bash
time ./grade2.py test-images/a-3.jpg output_images/a-3output.jpg a-3output.txt
time ./grade2.py test-images/a-27.jpg a-27output.jpg a-27output.txt
time ./grade2.py test-images/a-30.jpg a-30output.jpg a-30output.txt
time ./grade2.py test-images/a-48.jpg a-3output.jpg a-48output.txt
time ./grade2.py test-images/b-13.jpg b-13output.jpg b-13output.txt
time ./grade2.py test-images/b-27.jpg b-27output.jpg b-27output.txt
time ./grade2.py test-images/c-18.jpg c-18output.jpg c-18output.txt
time ./grade2.py test-images/c-33.jpg c-33output.jpg c-33output.txt
diff -y --suppress-common-lines a-3output.txt test-images/a-3_groundtruth.txt
diff -y --suppress-common-lines a-27output.txt test-images/a-27_groundtruth.txt
diff -y --suppress-common-lines a-30output.txt test-images/a-30_groundtruth.txt