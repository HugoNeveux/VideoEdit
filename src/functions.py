import cv2
import numpy as np
from progress.bar import Bar
import time

def video_overlay(video_path, image_path, begin=0, end=0, output_file='out.avi'):
    ########## Reading video ########## 
    cap = cv2.VideoCapture(video_path) # Reading base video

    ########## Read and configure image and masks ##########
    overlay = cv2.imread(image_path, -1)    # Opening overlay

    mask = overlay[:,:,3]   # Creating mask
    mask_inv = cv2.bitwise_not(mask)    # Creating inverted mask

    overlay = overlay[:,:,0:3]  # PNG conversion to BGR

    rows, cols, channels = overlay.shape    # Overlay properties

    ########## Creating VideoWriter object for output ##########
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_file[0], fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    ########## Other ##########
    success = True  # Initializing success variable

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    bar = Bar('Adding overlay...', max=frame_count) # Creating progress bar 

    ########## Main loop ##########
    while success:
        success, frame = cap.read() # Reading video frame
        if np.shape(frame) == ():   # If frame isn't empty
            break
        bar.next()  # Bar progress
        roi = frame[0:rows, 0:cols] 
        bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
        fg = cv2.bitwise_and(overlay, overlay, mask = mask)
        
        dst = cv2.add(bg, fg)   # Add overlay (fg) to background (bg)

        frame[0: rows, 0: cols] = dst
        out.write(frame)    # Writing frame with overlay to output

    bar.finish()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

