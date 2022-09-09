# import the necessary packages
from tkinter import Y
from imutils.video import VideoStream
import numpy as np
import argparse
import datetime
import imutils
import time
from time import sleep
import cv2
import yaml
from yaml.loader import SafeLoader
############################# Read the YAML file ################################################
stream = open ("config.yaml", 'r')
dictionary = yaml.load(stream, Loader=SafeLoader)

 
def threshold_num():
    threshold_1 = dictionary['threshold']
    print (type(threshold_1))
    threshold_1 = int(threshold_1)
    return threshold_1

def refrash_fn():
    refrash_frame = dictionary['refrash_frame']
    # print (type(refrash_frame))
    refrash_frame = int(refrash_frame)
    return refrash_frame

def img_direc():
    img_directory = dictionary['img_directory']
    # print (type(img_directory))
    img_directory = str(img_directory)
    return img_directory

def frame_params():
    params = dictionary['red_frame']
    # print(params) 
    params = dict(params)

    X = params['X']
    x_start = X ['x_start']
    x_end = X ['x_end']

    Y = params['Y']
    y_start = Y ['y_start']
    y_end = Y ['y_end']

    return x_start, x_end, y_start, y_end

def colors():
    color = dictionary['color']
    # print(type(color))
    color = dict(color)

    red = color['red']
    green = color['green']
    blue = color['blue']
    return red, green, blue

###########################################################################################


def image_cap(full_frame):
    img_directory = img_direc()
    date = time.strftime("%Y-%b-%d_(%H%M%S)")
    # full_frame = imutils.resize(full_frame, width=2048)
    # filename = 'C:/Users/user/OneDrive/Desktop/test/{0}.jpg'.format(date)
    filename = f'{img_directory}/{date}.jpg'
    cv2.imwrite(filename, full_frame)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())
vs = VideoStream(src=0).start()
time.sleep(1.0)
firstFrame = None
i = 0



if __name__ == '__main__':

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        x_start, x_end, y_start, y_end = frame_params()
        red, green, blue = colors()
        frame = vs.read()
        full_frame = frame
        frame = frame if args.get("video", None) is None else frame[1]
        text = "Not Detected"
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # show the trigger zone in red rectangle 
        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (blue, green, red), 2)            
        # cv2.rectangle(frame, (X, Y), (Xend, Yend), (BLUE, GREEN, RED), 2)

        # small RED frame
        frameDelta_RED = cv2.absdiff(firstFrame[y_start:y_end, x_start:x_end], gray[y_start:y_end, x_start:x_end])
        thresh_RED = cv2.threshold(frameDelta_RED, 25, 255, cv2.THRESH_BINARY)[1]

        # Sens of the motion ditection
        thresh_sum_RED = np.sum(thresh_RED)

        try:
            threshold_1 = threshold_num
            # Define threshold
            if thresh_sum_RED > threshold_1:
                text = "Detected"
                image_cap(full_frame)


            i += 1
            refrash_frame = refrash_fn
            if (i > refrash_frame):                                      # The number of frames from a sample.
                firstFrame = gray
                i = 0
                thresh_sum_RED = 0
        except:
            continue


        # draw the text and timestamp on the frame
        cv2.putText(frame, "Motion: {}".format(text), (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        #     cv2.imshow("Thresh", thresh)
        #     cv2.imshow("Frame Delta", frameDelta)

        key = cv2.waitKey(1) & 0xFF
        print(thresh_sum_RED)



