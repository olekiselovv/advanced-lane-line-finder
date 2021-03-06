import glob

import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_processing.calibration import calibrate_camera
from image_processing.image_processing import find_line_edges
from image_processing.transform import perspective_transform
from image_processing.lane_histogram import hist

chessboard_images = glob.glob('../data/main/camera_cal/*.jpg')
nx = 9  # chessboard corners in x direction
ny = 6  # chessboard corners in y direction
calibration_result = calibrate_camera(chessboard_images, (nx, ny))
mtx = calibration_result["mtx"]
dist = calibration_result["dist"]
img = cv2.imread('../data/main/test_images/test5.jpg')
undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
img_rgb = cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2RGB)
binary = find_line_edges(undistorted_img)
lines_img = np.dstack((binary, binary, binary)) * 255

warped, M, Minv, src, dst = perspective_transform(binary)

histogram = hist(warped)

plt.plot(histogram)
plt.show()
