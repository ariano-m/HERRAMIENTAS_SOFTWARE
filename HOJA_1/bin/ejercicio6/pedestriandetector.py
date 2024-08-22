"""
    Adrián Riaño Martínez
    Hoja de problemas 1
    Ejercicio 6
    python pedestriandetector.py --in ../datasets/pedestrian.avi
                                 --out ./outputs/pedestrian.avi
"""

import cv2 as cv
import argparse
import os


def detect_and_draw(hog, frame):
    try:
        rects, _ = hog.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=0.5)
        for (x, y, w, h) in rects:  # loop over all rectangules and draw it in frame
            frame = cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return frame
    except Exception as e:
        print(e)
        return frame


def write_video(out, processed_frames_l):
    """
        function that given a path and a list of frames, it saves the video
    :param out:
    :param processed_frames_l:
    :return:
    """
    fourcc = cv.VideoWriter.fourcc('X', 'V', 'I', 'D')   # set codec
    width = processed_frames_l[0].shape[1]
    height = processed_frames_l[0].shape[0]
    fps = 20
    fp = cv.VideoWriter(out, fourcc, fps, (width, height))
    for i in processed_frames_l:
        fp.write(i)
    fp.release()


def main(args):
    video = args['in']
    out = args['out']

    if not os.path.exists(video):
        Exception("video no exits")

    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
    cap = cv.VideoCapture(video)

    processed_frames_l = []
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        img = detect_and_draw(hog, frame)
        cv.imshow('frame', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        processed_frames_l.append(img)

    if 'out' in args and len(processed_frames_l) > 0:
        write_video(out, processed_frames_l)


if __name__ == "__main__":
    desc = 'pedestrian detector'
    parser = argparse.ArgumentParser(description=desc)

    commom_params = {'type': str, 'nargs': 1, 'required': True}
    parser.add_argument('--in', help='video input', **commom_params)
    parser.add_argument('--out', help='video output', **commom_params)

    args = {i: j[0] for i, j in vars(parser.parse_args()).items() if j is not None}

    main(args)
