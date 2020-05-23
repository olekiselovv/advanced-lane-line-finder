import glob

import cv2
import matplotlib.pyplot as plt
import numpy as np

from image_processing.calibration import calibrate_camera
from image_processing.image_processing import find_line_edges


def pipeline(img_path):
    chessboard_images = glob.glob('../data/main/camera_cal/*.jpg')
    nx = 9  # chessboard corners in x direction
    ny = 6  # chessboard corners in y direction
    calibration_result = calibrate_camera(chessboard_images, (nx, ny))
    mtx = calibration_result["mtx"]
    dist = calibration_result["dist"]
    # Apply a distortion correction to raw images

    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
    binary = find_line_edges(undistorted_img, yellow_thresh=(155, 255), white_thresh=((230, 230, 230), (255, 255, 255)))
    line_edges = np.dstack((binary, binary, binary)) * 255
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
    f.tight_layout()
    ax1.imshow(img_rgb)
    ax1.set_title('Original Image', fontsize=50)
    ax2.imshow(line_edges, cmap='gray')
    ax2.set_title('Combined Threshold', fontsize=50)
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)


images = glob.glob('../data/main/test_images/*.jpg')
for image in images:
    pipeline(image)
plt.show()