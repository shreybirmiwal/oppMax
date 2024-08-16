# Gen steps
#1. take pic every min
#2. process with LLM
    # extract: 1. activity, 2. time, 3. health and self score, 4. career score, 5. social score, 6. alternate oppurtunity cost that was most benefit
#3. save to firebase database


  
import cv2
import time
from datetime import datetime

def capture_image():
    cap = cv2.VideoCapture(0)
    
    ret, frame = cap.read()

    if ret:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"image_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
    else:
        print("Error: Could not read frame.")

    cap.release()

def main():
    while True:
        capture_image()
        time.sleep(60)

if __name__ == "__main__":
    main()