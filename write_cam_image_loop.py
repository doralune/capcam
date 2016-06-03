#coding: utf-8
import os
import sys
import argparse
import pdb
import cv2
import shutil
import threading
import time

def init(args):
    if 1 == args.user_param:
        set_user_param(args)
    pass

def set_user_param(args):
    raw = raw_input('Insert out_tmp_file(%s): ' % args.out_tmp_file) or args.out_tmp_file
    args.out_tmp_file = raw

    raw = raw_input('Insert out_file(%s): ' % args.out_file) or args.out_file
    args.out_file = raw

    raw = raw_input('Insert cam_index(%s): ' % args.cam_index)
    try:
        raw = int(raw)
    except:
        raw = args.cam_index
    raw = 0 if raw < 0 else raw
    args.cam_index = raw
    
    raw = raw_input('Insert image_size(%s): ' % args.image_size)
    try:
        raw = int(raw)
    except:
        raw = args.image_size
    raw = 256 if raw <= 0 else raw
    args.image_size = raw

    raw = raw_input('Insert grayscale(%s): ' % args.grayscale)
    try:
        raw = int(raw)
    except:
        raw = args.grayscale
    raw = 0 if raw not in range(2) else raw
    args.grayscale = raw

    raw = raw_input('Insert keep_aspect(%s): ' % args.keep_aspect)
    try:
        raw = int(raw)
    except:
        raw = args.keep_aspect
    raw = 1 if raw not in range(2) else raw
    args.keep_aspect = raw

    raw = raw_input('Insert mirror(%s): ' % args.mirror)
    try:
        raw = int(raw)
    except:
        raw = args.mirror
    raw = 0 if raw not in range(2) else raw
    args.mirror = raw

def run2(args):
    tar_s = args.image_size

    # find device id from ls /dev/video*
    print('Finding device ...')
    cap = cv2.VideoCapture(args.cam_index)
    pause_flag = False
    print('Found device')

    while True:
        if pause_flag is not True:
            ret, frame = cap.read()
            if 1 == args.grayscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if tar_s is not None:
                if 1 == args.keep_aspect: 
                    w, h, _ = frame.shape
                    sc = float(tar_s) / float(max(w, h))
                    frame = cv2.resize(frame, None, None, fx=sc, fy=sc)
                else:
                    w = h = tar_s
                    frame = cv2.resize(frame, (w, h))

            #if args.mirror is True:
                #frame = frame[:,::-1]

            # Display
            cv2.imshow('camera capture', frame)
            # Write
            cv2.imwrite(args.out_tmp_file, frame)
            shutil.copy(args.out_tmp_file, args.out_file)

        k = cv2.waitKey(1) & 0xFF # wait 1 msec
        # Break if ESC or q is pressed
        if k == 27 or k == ord('q'):
            break
        if k == ord('p'):
            pause_flag = not pause_flag

    cap.release()
    cv2.destroyAllWindows()

def run(args):
    # Print arguments
    for key in dir(args):
        if key[0] == '_':
            continue
        val = getattr(args, key)
        print('%s: %s' % (key, val))

    run2(args)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # out
    parser.add_argument("--out-file", dest="out_file", default='out.jpg')
    parser.add_argument("--out-tmp-file", dest="out_tmp_file", default='tmp.jpg')

    # in
    parser.add_argument("--user-param", dest="user_param", type=int, default=0)
    parser.add_argument("--cam-index", dest="cam_index", type=int, default=0)
    parser.add_argument("--image-size", dest="image_size", type=int, default=256)
    parser.add_argument("--grayscale", dest="grayscale", type=int, default=0, choices=range(2))
    parser.add_argument("--keep-aspect", dest="keep_aspect", type=int, default=1, choices=range(2))
    parser.add_argument("--mirror", dest="mirror", type=int, default=0, choices=range(2))

    args = parser.parse_args()

    init(args)
    #pdb.set_trace()
    run(args)
