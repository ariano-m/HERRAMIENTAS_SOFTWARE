"""
    Adrián Riaño Martínez
    Hoja de problemas 1
    Ejercicio 5
    python eyefacedetector.py --video ../datasets/eye_face/Avengers.mp4
                              --out ./outputs/ayefacedetector.avi
"""

import cv2 as cv
import argparse
import os


def detect_and_draw(eye_cascd, face_cascd, frame):
    """
        fucntion for detecting faces and eyes and drawing detected elements
    :param eye_cascd:
    :param face_cascd:
    :param frame:
    :return:
    """
    for cascd in [eye_cascd, face_cascd]:  # loop over eye and faces cascade
        rects = cascd.detectMultiScale(frame,
                                       scaleFactor=1.1,
                                       minNeighbors=5,
                                       minSize=(30, 30),
                                       flags=cv.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in rects:  # draw detected rectangles
            frame = cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0))

    return frame


def write_video(out, processed_frames_l):
    """
        function that given a path and a list of frames, it saves the video
    :param out:
    :param processed_frames_l:
    :return:
    """
    fourcc = cv.VideoWriter.fourcc('X', 'V', 'I', 'D')  # set codec
    width = processed_frames_l[0].shape[1]
    height = processed_frames_l[0].shape[0]
    fps = 20
    fp = cv.VideoWriter(out, fourcc, fps, (width, height))
    for i in processed_frames_l:
        fp.write(i)
    fp.release()


def main(args):
    video = args['video']
    out = args['out']

    if not os.path.exists(video):
        Exception("video no exits")

    eyes_xml = '../datasets/eye_face/haarcascade_eye.xml'
    cascade_eye = cv.CascadeClassifier(eyes_xml)
    face_xml = '../datasets/eye_face/haarcascade_frontalface_default.xml'
    cascade_face = cv.CascadeClassifier(face_xml)

    cap = cv.VideoCapture(video)
    processed_frames_l = []
    while True:
        ret, frame = cap.read()

        if not ret:  # if not data, leave from infinity loop
            break

        img = detect_and_draw(cascade_eye, cascade_face, frame)
        cv.imshow('frame', img)  # show image in windows
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        cv.imshow('ventana', img)
        processed_frames_l.append(img)

    if len(processed_frames_l) > 0:
        write_video(out, processed_frames_l)


if __name__ == "__main__":
    desc = 'eye and face detector'
    parser = argparse.ArgumentParser(description=desc)

    commom_params = {'type': str, 'nargs': 1, 'required': True}
    parser.add_argument('--video', help='video source', **commom_params)
    parser.add_argument('--out', help='video output', **commom_params)

    args = {i: j[0] for i, j in vars(parser.parse_args()).items() if j is not None}

    main(args)
