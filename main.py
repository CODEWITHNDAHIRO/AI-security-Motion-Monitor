from datetime import datetime
import cv2
import time

def monitor():
    cap = cv2.VideoCapture(0) # 0 is the Mac's built-in camera
    background_frame = None

    print("Security Monitor Active... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Pre-process (Grayscale and Blur)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # 2. Setting the background if it's the first frame
        if background_frame is None:
            background_frame = gray
            continue

        # 3. Computing the absolute difference
        frame_delta = cv2.absdiff(background_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # 4. Finding contours (the "motion")
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 500: # Ignore tiny movements like dust/noise
                continue
            
            # Motion Detected!
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("MOTION DETECTED")
                  # Add this inside the loop:
            with open("motion_log.txt", "a") as f:
                f.write(f"Motion detected at: {time.ctime()}\n")

        # 5. Create a Status Overlay
        status_text = "Status: IDLE"
        status_color = (0, 255, 0) # Green
            
        if len(contours) > 0:
            for contour in contours:
                if cv2.contourArea(contour) > 500:
                    status_text = "Status: MOTION DETECTED"
                    status_color = (0, 0, 255) # Red
        
        # Draw a black bar at the top for text
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
        
        # Add the text
        cv2.putText(frame, status_text, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        # Add a timestamp to the feed
        timestamp_str = time.strftime("%H:%M:%S")
        cv2.putText(frame, timestamp_str, (frame.shape[1] - 150, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        cv2.imshow("Security Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    monitor()
