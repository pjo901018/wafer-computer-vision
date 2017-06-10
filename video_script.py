import cv2
import time

import numpy as np

from logics.contour.contour_detector import detectContour
from logics.middleware.featuremap_converter import convertFeatureMap
from logics.region.InterestRegionFinder import findInterestRegion
from models.line import Line
from utils.visualize.videoloader import VideoLoader
from utils.visualize.windowmanager import WindowManager

video = VideoLoader.getInstance()
windowManager = WindowManager.getInstance()
windowManager.addWindow(['UP_1',
                         'UP_2',
                         'UP_3',
                         'UP_4',
                         'DOWN_1',
                         'DOWN_2',
                         'DOWN_3',
                         'DOWN_4'])

a = Line((20,15), (40,20))
mask = np.zeros((1080,1920,3))
# shape=(1080, 1920, 3)
Line.drawLines(mask, a.baseline)
# windowManager.imgshow(mask, 'original')

while True:
    frame = video.next()
    if frame is None:
        break

    windowManager.imgshow(frame, 'UP_1')

    interest = findInterestRegion(frame)
    windowManager.imgshow(interest, 'UP_2')

    gradient_, overwrite, _ = convertFeatureMap(frame, 'gradienty')
    windowManager.imgshow(gradient_, 'DOWN_3')
    canny_, overwrite, _ = convertFeatureMap(frame, 'canny')
    windowManager.imgshow(canny_, 'UP_3')
    fast_, overwrite, _ = convertFeatureMap(frame, 'fast')
    windowManager.imgshow(fast_, 'UP_4')
    feature, _, mainline = convertFeatureMap(canny_, 'hough')
    windowManager.imgshow(feature, 'DOWN_1')
    feature, _, mainline = convertFeatureMap(fast_, 'hough')
    windowManager.imgshow(feature, 'DOWN_2')
    feature, _, mainline = convertFeatureMap(gradient_, 'hough')
    windowManager.imgshow(feature, 'DOWN_4')

    # feature = detectContour(frame)

    # windowManager.imgshow(overwrite, '3')
    # windowManager.imgshow(mainlineboundary, '4')
    # subtracked = subtractBackground(frame)
    # windowManager.imgshow(subtracked, 'subtracked')
    # corner = detectCornerWithFAST(frame)
    # windowManager.imgshow(corner, 'corner')
    # corner = detectCornerWithShiTomasi(frame)
    # corner = detectCornerWithHarris(frame)
    # windowManager.imgshow(corner, 'surf')
    # contour = detectContourLine(frame)
    # windowManager.imgshow(contour, 'contourvideo')


    second = 1
    time.sleep(second)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()