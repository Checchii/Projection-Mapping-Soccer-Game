import cv2
import numpy as np

# List variable to store hsv pixel values
vals = []

# callback function
def on_mouse(event, x, y, flags, param):
    # check if the event was the left mouse button being clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the BGR pixel value at the clicked location
        # OpenCV represents RGB as BGR
        pixel = param[y, x]

        # Convert BGR to HSV and print the pixel values
        hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)
        print("HSV:", hsv_pixel[0][0])

        # Append the pixel value to the value list
        vals.append(hsv_pixel[0][0])

def get_tresh_from_vals(vals: np.array) -> np.array:
    # Calculate the min and max values for each channel
    min_h, min_s, min_v = np.min(vals, axis=0)
    max_h, max_s, max_v = np.max(vals, axis=0)

    lower_color = [min_h, min_s, min_v]
    upper_color = [max_h, max_s, max_v]

    # Output the results
    print(f"Lower bound: {lower_color}")
    print(f"Uppder bound: {upper_color}")

    return lower_color, upper_color
