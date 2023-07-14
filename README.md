# Vision_Algorithms_for_Mobile_Robotics_Wireframe_Cube
The purpose of this exercise is to place a virtual cube on a video of a planar grid viewed from different directions. It also helps you learn about the basics of perspective projection, changing coordinate systems, and lens distortion, as well as basic image processing.

## Cube.py
- Written for cube drawing on the chessboard.

- ![image](https://github.com/DoganK01/Vision_Algorithms_for_Mobile_Robotics_Wireframe_Cube/assets/98788987/6e065869-644e-4086-aa18-4ecc54da4c67)
## Dist_save.py
- Written for saving by applying undistortion process to distorted images.
## Dist_show.py
- Written to show undistorted images.

![image](https://github.com/DoganK01/Vision_Algorithms_for_Mobile_Robotics_Wireframe_Cube/assets/98788987/324456e2-eaae-4229-83ba-28cfdd301e2b)

## cornerDetection.py
- Written to detect corners on the chessboard on distorted images.
![image](https://github.com/DoganK01/Vision_Algorithms_for_Mobile_Robotics_Wireframe_Cube/assets/98788987/d855362e-f44e-4d3a-a2e6-32c3c6cee882)

## Algorithm
1. Read the undistorted images
2. Initialize the cube coods in World Frame.
3. Detect corners
4. Estimate rotation and  translation vectors (Or you can use them from poses.txt).
5. Project the  points cube in the image frame, using perspective projection.
6. Connect the points to form a cube.

## References
https://rpg.ifi.uzh.ch/teaching.html

