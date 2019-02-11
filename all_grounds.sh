#!/bin/bash
echo "a_3"
diff -y --suppress-common-lines a-3output.txt test-images/a-3_groundtruth.txt
echo "a_27"
diff -y --suppress-common-lines a-27output.txt test-images/a-27_groundtruth.txt
echo "a_30"
diff -y --suppress-common-lines a-30output.txt test-images/a-30_groundtruth.txt
echo "a_48"
diff -y --suppress-common-lines a-48output.txt test-images/a-48_groundtruth.txt
echo "b_13"
diff -y --suppress-common-lines b-13output.txt test-images/b-13_groundtruth.txt
echo "b_27"
diff -y --suppress-common-lines b-27output.txt test-images/b-27_groundtruth.txt
echo "c_18"
diff -y --suppress-common-lines c-18output.txt test-images/c-18_groundtruth.txt
echo "c_33"
diff -y --suppress-common-lines c-33output.txt test-images/c-33_groundtruth.txt
