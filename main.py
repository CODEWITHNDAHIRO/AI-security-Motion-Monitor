import cv2
import time

def monitor():
    cap = cv2.VideoCapture(0) # 0 is your Mac's built-in camera
    background_frame = None

    print("Security Monitor Active... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Pre-process (Grayscale and Blur)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # 2. Set the background if it's the first frame
        if background_frame is None:
            background_frame = gray
            continue

        # 3. Compute the absolute difference
        frame_delta = cv2.absdiff(background_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # 4. Find contours (the "motion")
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 500: # Ignore tiny movements like dust/noise
                continue
            
            # Motion Detected!
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("MOTION DETECTED")

        cv2.imshow("Security Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    monitor()
