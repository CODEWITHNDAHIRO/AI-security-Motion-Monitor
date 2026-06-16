import cv2
import datetime
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(filename, timestamp):
    try:
        message = "Motion detected at " + timestamp
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=5
        )
        with open(filename, "rb") as f:
            requests.post(
                "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendPhoto",
                data={"chat_id": TELEGRAM_CHAT_ID},
                files={"photo": f},
                timeout=5
            )
        print("Telegram alert sent: " + filename)
    except Exception as e:
        print("Telegram alert failed: " + str(e))

def monitor():
    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    last_alert_time = 0
    alert_cooldown = 10

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        fgmask = fgbg.apply(frame)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                motion_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break
        if motion_detected:
            current_time = time.time()
            if current_time - last_alert_time > alert_cooldown:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = "alerts/motion_" + timestamp + ".jpg"
                os.makedirs("alerts", exist_ok=True)
                cv2.imwrite(filename, frame)
                send_telegram_alert(filename, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                last_alert_time = current_time
                print("MOTION DETECTED")
        cv2.imshow("Motion Monitor", frame)
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    monitor()
