import cv2
import numpy as np
from progress.bar import Bar

def resize_video(video_path, output_file='out.avi', ratio=-1, conserve_ratio=False):
    """ A function which resizes a video """
    ########## Reading video ##########
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    framerate = cap.get(cv2.CAP_PROP_FPS)

    ########## Output ratio ##########
    if 0 <= ratio <= 100:
        ratio_width = int(cap.get(3) * ratio)
        ratio_height = int(cap.get(4) * ratio)
    else:
        return print("[X] You must provide a valid ratio number (float between 0 and 100).")

    dsize = (ratio_width, ratio_height)

    ########## VideoWriter object for output ##########
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'MJPG'), framerate, dsize)

    ########## Other ##########
    success = True

    bar = Bar('Resizing video...', max=frame_count) # Creating progress bar 
    
    ########## Main loop ##########
    while success:
        success, frame = cap.read()
        if np.shape(frame) == ():
            break
        bar.next()
        resized = cv2.resize(frame, dsize)
        out.write(resized)

    bar.finish()

    cap.release()
    out.release()
    cv2.destroyAllWindows()
