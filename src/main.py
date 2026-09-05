# Run python3 main.py in terminal
import cv2
import numpy as np
import get_hsv as hsv

# Threshold Values for Pink and Lime Mask
pink_low = np.array([120, 120, 80])
pink_up = np.array([190, 175, 255])

lime_low = np.array([20, 110, 150])
lime_up = np.array([55, 210, 220])

# Open a connection to the webcam (0 is default, change index for different cameras)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame by frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Generate the Masks
    pink_mask = cv2.inRange(hsv_frame, pink_low, pink_up)
    lime_mask = cv2.inRange(hsv_frame, lime_low, lime_up)

    # Combine the masks into one with bitwise OR
    result = cv2.bitwise_or(pink_mask, lime_mask)

    # Display the Frames
    cv2.imshow("frame", frame)
    cv2.imshow("Results", result)

    # Left Click To Get Pixel HSV values
    cv2.setMouseCallback('frame', hsv.on_mouse, frame)
    
    # Break the loop if Q is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release the capture when done
cap.release()
cv2.destroyAllWindows()