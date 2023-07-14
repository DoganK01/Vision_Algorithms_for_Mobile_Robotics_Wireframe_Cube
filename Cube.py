import numpy as np
import cv2
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def drawBoxes(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)
    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)
    # draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)
    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), 3)
    return img

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
fps = 30
frame_size = (640, 480)
output_video = cv2.VideoWriter('outputPnP.avi', fourcc, fps, frame_size)


K = np.loadtxt('data/K.txt')
dist = np.array([-1.6774e-06, 2.5847e-12, 0.0, 0.0, 0.0])  # Values of D.txt
# print(dist)
poses = np.loadtxt('data/poses.txt')


chessboard_width = 9
chessboard_height = 6
chessboard_size = (chessboard_width, chessboard_height)


# objp represents the 3D world coordinates of the chessboard corner points. Since the board is planar, the z axis is always zero. It is used to calibrate the camera and determine its position.
objp = np.zeros((chessboard_width * chessboard_height, 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_width, 0:chessboard_height].T.reshape(-1, 2)

# print(objp)

rvec = np.reshape(poses[0, :3], (3,1)) # or transpose it. These are for first image.
tvec = np.reshape(poses[0, 3:], (3,1))

# the position of the cube to be drawn on the board is determined.
axisBoxes = np.float32([[0,0,0], [0,2,0], [2,2,0], [2,0,0],
                   [0,0,-2],[0,2,-2],[2,2,-2],[2,0,-2] ])

# images = glob.glob('data/images_undistorted/*.jpg')
for idx, image_path in enumerate(sorted(glob.glob('data/images_undistorted/undistorted_img_*.jpg'))):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rvec = np.reshape(poses[idx, :3], (3,1))
    # this function is used to detect a chessboard pattern with given dimensions within an image.
    # the function takes as input a grayscale image, the dimensions of the chessboard, and an output parameter.
    # returns an array containing the position of detected vertices as output
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

    # used to find the precise location of the vertices found by cv.findChessboardCorners.
    # it takes as input a grayscale image, the positions of the corners, and a set of adjustment parameters.
    # the function returns an array containing the precise position of the detected vertices.
    # we use this function for undistorted image. If we have distortion images, we can use just variable "corners" coming from cv.findChessboardCorners() instead of corners2
    # for cv2.soolvePnP.
    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    # print(corners2.shape)
    # get pose for the current frame
    # rvec, tvec = poses[idx, :3], poses[idx, 3:]


    # it's used to estimate the camera position using the 3D model of an object and the 2D image points contained in an image.
    # it takes as input the object's 3D point cloud, 2D image points, camera matrix and distortion coefficients.
    # as output, it returns the rotation vector (rvecs) and the translation vector (tvecs) that determine the camera position and orientation.
    ret, rvecs, tvecs = cv2.solvePnP(objp, corners2, K, dist)  # we could just take first index of "poses" for rvec and tvec.
    print(rvecs) #[[-0.37123714]
    # [ 0.03966002]
    # [ 0.06545071]] shape: (3,1)
    print(tvecs) # [[-2.67436769]
    # [-3.67902726]
    # [ 9.96128249]] shape: (3,1)
    print(rvec) # [[-0.37248319]
    # [ 0.03970225]
    # [ 0.06503934]] shape: (3,1)
    print(tvec) # [[-0.10703586]
    # [-0.14706524]
    # [ 0.3985125 ]] shape: (3,1)   # !!! IMPORTANT NOTE: There is a huge difference between tvecs and tvec.
    # I couldn't figure out why. Instead of using poses.txt, I used this function to solve the pose problem.

    # project 3D points to image plane
    # this function is used to project 3D object points onto the image plane.
    # it takes as input the 3D points, the rotation vector (rvecs), the translation vector (tvecs), the camera matrix, and the distortion coefficients that determine the camera position and orientation.
    # returns an array containing the projection of 3D points onto the image plane as output.
    imgpts, jac = cv2.projectPoints(axisBoxes, rvecs, tvecs, K, dist)  # you can use rvec or rvecs. Both are roughly the same value.
    # about variable "jac": helps in understanding the sensitivity of the projected points to changes in the camera pose parameters.

    img = drawBoxes(img, corners2, imgpts)
    # name = f'img{idx}'
    cv2.imshow("Cube", img)
    cv2.waitKey(0)
    # output_video.write(img)


cv2.destroyAllWindows()

# output_video.release()


