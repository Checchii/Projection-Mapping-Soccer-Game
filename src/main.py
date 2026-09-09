# Run python3 main.py in terminal
import os
import cv2
import numpy as np
import get_hsv as hsv

# Get Absolute Directory Path of Project
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Find PNG File
img_path = os.path.join(current_dir, "assets", "soccer_goal.png")

# Soccer Net Image
img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

# Check Image Loading
if img is None:
    print("Error: Could not load the image, check file path.")
else:
    # Get the Original Dimensions
    height, width = img.shape[:2]

    # Calculate Specific Aspect Ratio
    desired_width = 1000
    aspect_ratio = desired_width / float(width)
    desired_height = int(height * aspect_ratio)

    # Resize the Image
    resized_img = cv2.resize(img, (desired_width, desired_height))

    # Print Dimensions of Resized Image to Calculate Destination Coordinates (560, 140)
    print(f"Dimensions: {resized_img.shape}")


# Threshold Values for Pink and Lime Mask
pink_low = np.array([120, 120, 90])
pink_up = np.array([200, 185, 255])

lime_low = np.array([30, 90, 100])
lime_up = np.array([95, 240, 250])


# Open a connection to the webcam (0 is default, change index for different cameras)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame by frame
    ret, frame = cap.read()
    if not ret:
        break

    # ---- Soccer Net Image Processing ----
    # Region of Interest (ROI)
    roi = frame[40:1040, 460:1460]
    
    # Split the 4 Channels of the Resized Image
    b, g, r, a = cv2.split(resized_img)
    # Combine BGR back into 3 Channel Image Dropping the Alpha
    merged_bgr = cv2.merge([b, g, r])
        
    # Create Two Masks For Soccer Net 
    opaque_goal = cv2.bitwise_and(merged_bgr, merged_bgr, mask=a)
    # Invert the Alpha Mask
    inverted_mask = cv2.bitwise_not(a)
    transparent_goal = cv2.bitwise_and(roi, roi, mask=inverted_mask)
    
    # Combine the Two Masks
    soccer_goal = cv2.add(opaque_goal, transparent_goal)

    # Reassign Soccer Net Image to ROI
    frame[40:1040, 460:1460] = soccer_goal


    # ---- Ball Detection ---- 
    # Convert frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Generate the Masks
    pink_mask = cv2.inRange(hsv_frame, pink_low, pink_up)
    lime_mask = cv2.inRange(hsv_frame, lime_low, lime_up)

    # Combine the masks into one with bitwise OR
    result = cv2.bitwise_or(pink_mask, lime_mask)

    # Apply Morphological Enclosing on Mask
    kernel = np.ones((30,30), np.uint8)
    ball = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)

    # Find Ball Contour
    contours, _ = cv2.findContours(ball, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Calculate Largest Contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
    
        # Calculate the Minimum Enclosing Circle
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        
        # Cast to Integer Coordinates for Pixel Perfect Drawing
        center = (int(x), int(y))
        radius = int(radius)
    
        # Draw the Circle on the Soccer Ball in Live Frame
        cv2.circle(frame, center, radius, (0,0,255), 2)
        
        # Draw Exact Center Point on Ball in Live Frame
        cv2.circle(frame, center, 2, (0,0,255), -1)

    
    # ---- Window Display ----
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
