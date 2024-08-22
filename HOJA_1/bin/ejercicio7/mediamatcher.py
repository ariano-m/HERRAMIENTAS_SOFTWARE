"""
    Adrián Riaño Martínez
    Hoja de problemas 1
    Ejercicio 7
    python mediamatcher.py --query ./inputs/logo/logo.png --covers ./inputs
"""

import matplotlib.pyplot as plt
import cv2 as cv
import argparse
import glob
import time


def main(args):
    start = time.time() * 1000  # for computing time execution program

    query = args['query']
    covers = args['covers']

    img1 = cv.imread(query, cv.IMREAD_GRAYSCALE)  # queryImage
    images_l = [cv.imread(i, cv.IMREAD_GRAYSCALE) for i in glob.glob(covers + '/*')]

    sift = cv.SIFT_create()  # Initiate SIFT detector

    best_img = None  #best image found
    best_good = []
    umbral = 10
    kp1, des1 = sift.detectAndCompute(img1, None)  # find the keypoints and descriptors with SIFT
    for idx, i in enumerate(images_l):
        try:
            kp2, des2 = sift.detectAndCompute(i, None)
            bf = cv.BFMatcher()  # BFMatcher with default params
            matches = bf.knnMatch(des1, des2, k=2)  # detect matches

            good = []  # Apply ratio test
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            img3 = cv.drawMatchesKnn(img1, kp1, i, kp2, good, None,
                                     flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            if len(good) > len(best_good) and len(good) >= umbral:  # update best image if conditios is True
                best_good = good
                best_img = img3
        except:
            print(f"image {idx} failed!")
    print(time.time() * 1000 - start)
    plt.imshow(best_img)
    plt.show()


if __name__ == "__main__":
    desc = 'media matcher'
    parser = argparse.ArgumentParser(description=desc)

    commom_params = {'type': str, 'nargs': 1, 'required': True}
    parser.add_argument('--query', help='source with images', **commom_params)
    parser.add_argument('--covers', help='output', **commom_params)

    args = {i: j[0] for i, j in vars(parser.parse_args()).items() if j is not None}

    main(args)
