"""
    Adrián Riaño Martínez
    Hoja de problemas 1
    Ejercicio 2
    python visual_tracking.py --images ../datasets/frames
                              --min_values 29 43 126
                              --max_values 88 255 255
                              --output visual_tracking.avi
"""
from tqdm import tqdm
import numpy as np
import cv2 as cv
import argparse
import glob
import os


def processing_image(image, range_hsv, previous_centoid) -> np.array:
    """
        fucntion for applying several operation to image and detecting the objects
    :param image:
    :param range_hsv:
    :param previous_centoid:
    :return:
    """
    def apply_gaussian_filter(img):
        """
            apply a gausian of (5,5)
        :param img:
        :return:
        """
        return cv.GaussianBlur(img, (5, 5), 1.0)

    def to_hsv(img):
        """
            transform rgb to hsv format
        :param img:
        :return:
        """
        return cv.cvtColor(img, cv.COLOR_RGB2HSV)

    def to_segmentate(img, intervals):
        """
            threshold the image according ranges
        :param img:
        :param intervals:
        :return:
        """
        lower_color = np.array(intervals[0], dtype='uint8')
        upper_color = np.array(intervals[1], dtype='uint8')
        return cv.inRange(img, lower_color, upper_color)  # to thershold image

    def remove_focus(img):
        """
            fucntion for removing the focus
        :param img:
        :return:
        """
        kernel = np.ones((3, 3), np.uint8)
        img_erosed = cv.erode(img, kernel, 2)
        return cv.dilate(img_erosed, kernel, 2)

    def detect_contours_and_get_max(img_):
        """
            fucntion for given a image, detect the contours and get the max size one
        :param img_:
        :return:
        """
        contours, hierarchy = cv.findContours(img_, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # search contours
        contours_area_l = [cv.contourArea(i) for i in contours]
        index_max = contours_area_l.index(max(contours_area_l))  # get the index with maximum contours
        return contours, index_max

    def draw(img, contour_l, index, prev_centroid):
        """
            fucntion for draw the calculated centroids
        :param img:
        :param contour_l:
        :param index:
        :param prev_centroid:
        :return:
        """

        img_with_cont = cv.drawContours(img, contour_l, contourIdx=index, color=(0, 0, 255), thickness=1)
        moment = cv.moments(contour_l[index])  # compute moments
        cx = int(moment["m10"] / moment["m00"])
        cy = int(moment["m01"] / moment["m00"])
        center = (cx, cy)  # centoid
        img_centroid = cv.circle(img_with_cont, center, 7, (0, 255, 0), -1)

        if prev_centroid is None:
            return img_centroid, center
        return cv.line(img_centroid, prev_centroid, center, (255, 0, 0)), center

    original = image.copy()
    gauss_img = apply_gaussian_filter(image)
    hsv_img = to_hsv(gauss_img)
    img_seg = to_segmentate(hsv_img, range_hsv)
    img_without_focus = remove_focus(img_seg)
    contour_l, index = detect_contours_and_get_max(img_without_focus)  # index -> position max contour
    return draw(original, contour_l, index, previous_centoid)


def write_video(out, processed_frames_l):
    """
        function that given a path and a list of frames, it saves the video
    :param out:
    :param processed_frames_l:
    :return:
    """
    fourcc = cv.VideoWriter.fourcc('X', 'V', 'I', 'D')  # set codec
    width = processed_frames_l[0].shape[1]  # get width
    height = processed_frames_l[0].shape[0]  # get height
    fps = 3
    fp = cv.VideoWriter(out, fourcc, fps, (width, height))
    for i in processed_frames_l:
        fp.write(i)
    fp.release()


def main(args):
    min_values = [int(i) for i in args['min_values']]  # get args
    max_values = [int(i) for i in args['max_values']]

    path_dataset = args['images']
    if not os.path.isdir(path_dataset):
        raise Exception("This path doesn't exit")

    images = glob.glob(f'{path_dataset}/*.jpg')
    processed_l, prev_centoid = [], None
    for i in tqdm(images):
        img, prev_centoid = processing_image(cv.imread(i), (min_values, max_values), prev_centoid)
        cv.imshow('img', img)
        processed_l.append(img)

    if 'output' in args and len(processed_l) > 0:
        write_video(args['output'], processed_l)


if __name__ == "__main__":
    desc = 'visual tracking script'
    parser = argparse.ArgumentParser(description=desc)

    args_values = {'nargs': '+', 'action': 'append', 'required': True, 'type': str}
    parser.add_argument('--images', nargs=1, type=str, required=True, help='source with images')
    parser.add_argument('--min_values', help='max values', **args_values)
    parser.add_argument('--max_values', help='max values', **args_values)
    parser.add_argument('--output', nargs='*', type=str, required=False, help='save files')

    args = {i: j[0] for i, j in vars(parser.parse_args()).items() if j is not None}

    main(args)
