
import cv2
from pyzbar.pyzbar import decode
import requests
import time

url = "http://127.0.0.1:5000/verify-ticket"

def read_qr_from_camera():
    cap = cv2.VideoCapture(0)
    print("وجهي الكود على الكاميرا...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        for barcode in decode(frame):
            ticket_id = barcode.data.decode("utf-8")
            print(f"QR مقروء: {ticket_id}")

            # إرسال الطلب إلى السيرفر
            payload = {
                "ticket_id": ticket_id
            }

            response = requests.post(url, json=payload)
            print("الرد من السيرفر:")
            print(response.status_code)
            print(response.text)

            time.sleep(3)  # انتظري شوي قبل محاولة جديدة

        cv2.imshow("Scan QR Code", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

read_qr_from_camera()
