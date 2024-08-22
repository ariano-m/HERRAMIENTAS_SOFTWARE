"""
    Adrián Riaño Martínez
    Hoja de problemas 1
    Ejercicio 7
    python mediamatcher.py --query ../../HOJA_PROBLEMAS_1/bin/inputs/logo/logo.png
                           --covers ../../HOJA_PROBLEMAS_1/bin/inputs
"""

import multiprocessing
import numpy as np
import cv2 as cv
import time
import glob
import sys

sift = cv.SIFT_create()
path = './dataset/logo/logo.png'
img1 = cv.imread(path, cv.IMREAD_GRAYSCALE)  # queryImage
kp1, des1 = sift.detectAndCompute(img1, None)


def fun(img):
    try:
        i = img
        kp2, des2 = sift.detectAndCompute(i, None)

        bf = cv.BFMatcher()  # BFMatcher with default params
        matches = bf.knnMatch(des1, des2, k=2)

        good = []  # Apply ratio test
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])

        img3 = cv.drawMatchesKnn(img1, kp1, i, kp2, good, None,
                                 flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        return img3, len(good)
    except:
        print("error")
        return np.array([]), 0


def main():
    start = time.time() * 1000
    path = './dataset'
    images_l = [cv.imread(i, cv.IMREAD_GRAYSCALE) for i in glob.glob(path + '/*')]

    best_img = None
    len_ = 0
    with multiprocessing.Pool(5) as p:
        output = p.map(fun, images_l)
        for i, j in output:
            if j > len_:
                len_, best_img = j, i
    sys.stdout.write(str(time.time() * 1000 - start))


if __name__ == '__main__':
    main()
