import cv2
import numpy as np
from progress.bar import Bar
import time

def video_overlay(video_path, image_path, begin, end, output_file='out.avi', x=0, y=0):
    ########## Reading video ########## 
    cap = cv2.VideoCapture(video_path) # Reading base video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    framerate = cap.get(cv2.CAP_PROP_FPS)
    video_width, video_height = int(cap.get(3)), int(cap.get(4))

    ########## Read and configure image and masks ##########
    overlay = cv2.imread(image_path, -1)    # Opening overlay

    mask = overlay[:,:,3]   # Creating mask
    mask_inv = cv2.bitwise_not(mask)    # Creating inverted 

    overlay = overlay[:,:,0:3]  # PNG conversion to BGR

    rows, cols, channels = overlay.shape    # Overlay properties

    # Check if image can fit into the video
    if cols >= video_width or rows >= video_height:
        return print("[X] The provided image is too large to fit into the video - Please resize it")
    elif x + cols >= video_width or y + rows >= video_height:
        return print("[X] The specified coords are too big - can't overlay the image here")

    ########## Creating VideoWriter object for output ##########
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_file[0], fourcc, framerate, (video_width, video_height))

    ########## Other ##########
    frame_counter = 0
    success = True  # Initializing success variable
    frame_min = int(round(framerate)) * begin 
    if end != 0:
        frame_max = int(round(framerate)) * end
    else:
        frame_max = frame_count

    bar = Bar('Adding overlay...', max=frame_count) # Creating progress bar 

    ########## Main loop ##########
    while success:
        success, frame = cap.read() # Reading video frame
        if np.shape(frame) == ():   # If frame isn't empty
            break
        bar.next()  # Bar progress
        frame_counter += 1
        if frame_min <= frame_counter <= frame_max:
            roi = frame[y:y+rows, x:x+cols] 
            bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
            fg = cv2.bitwise_and(overlay, overlay, mask = mask)
            
            dst = cv2.add(bg, fg)   # Add overlay (fg) to background (bg)

            frame[y:y+rows, x:x+cols] = dst
        out.write(frame)    # Writing frame with overlay to output

    bar.finish()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

