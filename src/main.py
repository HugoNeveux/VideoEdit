import cv2
import numpy as np

cap = cv2.VideoCapture('../testing_resources/video1.mp4') # Reading base video

overlay = cv2.imread('../testing_resources/image1.png')    # Opening the overlayed png
rows, cols, channels = overlay.shape    # Overlay properties

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('out.avi', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
success = True

cv2.imshow('overlay', overlay)

while success:
    success, frame = cap.read()
    if np.shape(frame) == ():
        break
    roi = frame[0:rows, 0:cols]
    cv2.imshow('a-1', roi)
    img2gray = cv2.cvtColor(overlay, cv2.COLOR_BGR2GRAY)
    cv2.imshow('a', img2gray)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    cv2.imshow('b', mask)
    mask_inv = cv2.bitwise_not(mask)
    cv2.imshow('c', mask_inv)
    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    fg = cv2.bitwise_and(overlay, overlay, mask=mask)
    cv2.imshow('d', bg)
    cv2.imshow('e', fg)

    dst = cv2.add(bg, fg)

    frame[0: rows, 0: cols] = dst
    cv2.waitKey(10)
    out.write(frame)


cap.release()
out.release()
cv2.destroyAllWindows()

