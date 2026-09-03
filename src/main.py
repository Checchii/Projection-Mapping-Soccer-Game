import cv2
import numpy as np
from get_hsv import on_mouse
# within src path run python3 main.py to run this script

# Open a connection to the webcam (0 is default, change index for different cameras)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame by frame
    ret, frame = cap.read()
    if not ret:
        break

    # Display the frame
    cv2.imshow("frame", frame)
    
    cv2.setMouseCallback('frame', on_mouse, frame)

    # Break the loop if Q is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release the capture when done
cap.release()
cv2.destroyAllWindows()