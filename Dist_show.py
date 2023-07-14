import cv2
import numpy as np
import glob
import os

with open('data/K.txt', 'r') as f:
    lines = f.readlines()
    K = np.array([[float(x) for x in line.split()] for line in lines])

with open('data/D.txt', 'r') as f:
    lines = f.readlines()
    D = np.array([float(x) for x in lines[0].split()])

with open('data/poses.txt', 'r') as f:
    lines = f.readlines()
    poses = np.array([[float(x) for x in line.split()] for line in lines])

D = np.append(D, 0)  # p1
D = np.append(D, 0)  # p2
D = np.append(D, 0)  # k3d

image_paths = glob.glob('data/images/*.jpg')

# output_folder = 'data/images_undistorted'
# os.makedirs(output_folder, exist_ok=True)

for img_path in image_paths:
    img = cv2.imread(img_path, 0)  # uploading image as grayscale
    h, w = img.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(K, D, (w, h), 1, (w, h))
    dst = cv2.undistort(img, K, D, None, new_camera_matrix)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    # output_path = os.path.join(output_folder, 'undistorted_' + os.path.basename(img_path))
    # cv2.imwrite(output_path, dst)
    cv2.imshow(f'Undistorted Images', dst)
    cv2.waitKey(0)

cv2.destroyAllWindows()

# This is a different undistortion operation. You can use this line of code. Just delete this above: dst = cv2.undistort(img, K, D, None, new_camera_matrix) and copy the code below.
mapx, mapy = cv2.initUndistortRectifyMap(K, D, None, new_camera_matrix, (w,h), 5)
dst2 = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)