# Removing Projective Distortion on Images
Images have inherent projective distortion which makes every rectangular objects appear distorted. In order to remove this projective distortion, a 3x3 homography matrix is needed to map the image from projective to affine. With the use of linear mapping and least squares estimation, the homography matrix can be solved given at least four points of reference to map into the four corners of the perspective corrected image.

The objective of this project is to remove the projective distortion on images by solving for the homography matrix and use that to perform linear transformation on the image, effectively removing the projective distortion in it. Firstly, an image will be shown on the UI and four corners of the rectangular object must be clicked to start the linear mapping proess. <b> Selecting the four corners of the rectangular object in the image must be done from top left, top right, bottom left, and bottom right respectively </b>. Once the fourth point has been selected, the program will then compute for the homography matrix, and then use that matrix to perform linear transformation. After that process, the perspective corrected image will be shown on the right of the input image. 

More test images can be tested to make sure that the program is working properly by adding it to the images folder in this repository (Don't forget to rename the file name in the main code). Currently, there are three provided images in the <i>images</i> folder that can be used for testing.

This program is undergraduate assignment on the class of CoE197U in University of the Philippines, Diliman. 

Created by: <b> Joshua B. Ramos </b>
