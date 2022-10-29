# Removing Projective Distortion on Images
# Created by: Joshua B. Ramos 
import cv2 
import numpy as np

# Initiate these variables
pts_selected = []
ctr = 0

# Functions
def shapeSelection(event, x, y, flags, param):
    global pts_selected, ctr

    if ctr == 4: # Once four corners are selected, close the window to perform the perspective correction
        cv2.destroyAllWindows()

    if event == cv2.EVENT_LBUTTONDOWN: # Record the clicked corners to pts_selected and mark it with a red square
        pts_selected.append((x, y))
        cv2.rectangle(image, (x+3,y+3), (x-3,y-3), color = (0,0,255))
        ctr += 1
        concatenated_img = np.hstack((image, result))
        cv2.imshow("Select four corners (Top Left -> Top Right -> Bottom Left -> Bottom Right)", concatenated_img)

def getax(x1, y1, x2, y2): # Supporting function for getA
    return np.array([-x1, -y1, -1, 0, 0, 0, x1*x2, y1*x2, x2])

def getay(x1, y1, x2, y2): # Supporting function for getA
    return np.array([0, 0, 0, -x1, -y1, -1, x1*y2, y1*y2, y2])

def getA(src, dst): # Make a system of linear equations of the form Ah = 0 using the selected corners to get homography matrix h
    for i in range(9):
        if i == 0:
            ax = getax(src[i][0],src[i][1],dst[i][0],dst[i][1])
            A = ax
        elif i == 8:
            A = np.vstack([A, np.array([0, 0, 0, 0, 0, 0, 0, 0, 1])])
        elif not(i % 2):
            ax = getax(src[i//2][0],src[i//2][1],dst[i//2][0],dst[i//2][1])
            A = np.vstack([A, ax])
        elif i % 2:
            ay = getay(src[i//2][0],src[i//2][1],dst[i//2][0],dst[i//2][1])
            A = np.vstack([A, ay])
    return A

def homographyMatrix(A): # Solve for h and reshape it to a 3x3 matrix
    h = np.array([[0],[0],[0],[0],[0],[0],[0],[0],[1]])
    h = np.matmul(np.linalg.inv(A),h)
    H = np.reshape(h, (3,3))
    return H

def linearTransformation(image, result, M): # Perform the mapping from image to result using a transformation matrix M
    for i in range(500):
        for j in range(707):
            xp = round((i*M[0][0]+j*M[0][1]+M[0][2])/(i*M[2][0]+j*M[2][1]+M[2][2]))
            yp = round((i*M[1][0]+j*M[1][1]+M[1][2])/(i*M[2][0]+j*M[2][1]+M[2][2]))
            if xp > 499 or xp < 0 or yp > 706 or yp < 0:
                continue
            else: 
                result[yp][xp] = image[j][i]
    return result

# Insert image and initialize the perspective corrected result
image = cv2.imread('images/test_img2.jpg')
image = cv2.resize(image,(500,707))
result = np.zeros([707,500,3],dtype=np.uint8)


# Display image and user should select four corners to map
clone = image.copy()
concatenated_img = np.hstack((image, result))
cv2.namedWindow("Select four corners (Top Left -> Top Right -> Bottom Left -> Bottom Right)")
cv2.imshow("Select four corners (Top Left -> Top Right -> Bottom Left -> Bottom Right)", concatenated_img)
cv2.setMouseCallback("Select four corners (Top Left -> Top Right -> Bottom Left -> Bottom Right)", shapeSelection)
print("Select four corners (Top Left -> Top Right -> Bottom Left -> Bottom Right)")
cv2.waitKey(0)
cv2.destroyAllWindows()

# Organize the source and destination corner points
src = np.array(pts_selected)
dst = np.array([[0,0],[500,0],[0,707],[500,707]])

# Get the 3x3 homography matrix that will map the image from perspective to affine
A = getA(src,dst)
M = homographyMatrix(A)

# Perform linear transformation using the acquired homography matrix
B = linearTransformation(clone, result, M)

# Display the perspective corrected image
concatenated_img = np.hstack((clone, B))
cv2.imshow("Perspective Correction", concatenated_img)
cv2.waitKey(0)
cv2.destroyAllWindows()




