import cv2
import numpy as np
from progress.bar import Bar
import time

def videoInit(video_path):
    """ A function to read video and get some infos about it """
    if video_path == "0":
        cap = cv2.VideoCapture(0)
        success, frame = cap.read()
        video_width, video_height, video_channels = frame.shape 
    else:
        cap = cv2.VideoCapture(video_path)
        video_width, video_height = int(cap.get(3)), int(cap.get(4))
    framerate = cap.get(cv2.CAP_PROP_FPS)
    return cap, framerate, video_width, video_height

def overlayImageInit(image_path):
    """ A function to read and create mask for overlay image """
    overlay = cv2.imread(image_path, -1)    # Opening overlay

    mask = overlay[:,:,3]   # Creating mask
    mask_inv = cv2.bitwise_not(mask)    # Creating inverted 

    overlay = overlay[:,:,0:3]  # PNG conversion to BGR

    rows, cols, channels = overlay.shape    # Overlay properties
    return overlay, mask, mask_inv, rows, cols


def videoOverlay(video_path, image_path, begin, end, output_file='out.avi', x=0, y=0):
    ########## Load video #########
    cap, framerate, video_width, video_height = videoInit(video_path)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    ######### Load overlay and create mask #########
    overlay, mask, mask_inv, rows, cols = overlayImageInit(image_path)

    # Check if image can fit into the video
    if cols >= video_width or rows >= video_height and video_path != "0":
        return print("[X] The provided image is too large to fit into the video - Please resize it")
    elif x + cols >= video_width or y + rows >= video_height and video_path != "0":
        return print("[X] The specified coords are too big - can't overlay the image here")

    ########## Creating VideoWriter object for output ##########
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_file, fourcc, framerate, (video_width, video_height))

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
        if video_path != "0":
            bar.next()  # Bar progress
        frame_counter += 1
        if frame_min <= frame_counter <= frame_max:
            roi = frame[y:y+rows, x:x+cols] 
            bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
            fg = cv2.bitwise_and(overlay, overlay, mask = mask)
            
            dst = cv2.add(bg, fg)   # Add overlay (fg) to background (bg)

            frame[y:y+rows, x:x+cols] = dst
        if video_path == "0":
            cv2.imshow("camera", frame)
            cv2.waitKey(10)
        out.write(frame)    # Writing frame with overlay to output

    bar.finish()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def webcamOverlay(image_path, output_file ,x=0, y=0):
    ########## Load video #########
    cap, framerate, video_width, video_height = videoInit("0")
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    ######### Load overlay and create mask #########
    overlay, mask, mask_inv, rows, cols = overlayImageInit(image_path)

    ########## Creating VideoWriter object for output ##########
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_file, fourcc, framerate, (video_width, video_height))

    if rows > cap.read()[1].shape[0] or cols > cap.read()[1].shape[1]:
        return print("[X] The provided image is too large to fit into the video - Please resize it")
    success = True

    ########## Main loop ##########
    while success:
        success, frame = cap.read() # Reading video frame
        if np.shape(frame) == ():   # If frame isn't empty
            break
        roi = frame[y:y+rows, x:x+cols] 
        bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
        fg = cv2.bitwise_and(overlay, overlay, mask = mask)
        
        dst = cv2.add(bg, fg)   # Add overlay (fg) to background (bg)

        frame[y:y+rows, x:x+cols] = dst
        cv2.imshow("camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        out.write(frame)    # Writing frame with overlay to output


    cap.release()
    out.release()
    cv2.destroyAllWindows()
