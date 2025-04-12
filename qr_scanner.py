import cv2
from pyzbar.pyzbar import decode
import requests
import json
import time

# URL of your Flask verification server
url = "http://127.0.0.1:5000/verify-ticket"

def read_qr_from_camera():
    cap = cv2.VideoCapture(0)
    print("📸 Starting camera... Please place the QR code in front of the camera.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        qr_codes = decode(frame)

        for qr in qr_codes:
            qr_data = qr.data.decode("utf-8")
            print(f"📦 QR Code detected: {qr_data}")

            try:
                ticket_json = json.loads(qr_data)  # make sure it's valid JSON

                response = requests.post(url, json=ticket_json)
                if response.status_code == 200:
                    print(f"✅ ACCESS GRANTED: {response.json()['message']}")
                else:
                    print(f"❌ ACCESS DENIED: {response.json()['message']}")
            except Exception as e:
                print("⚠️ Invalid QR code data or server error:", e)

            time.sleep(2)  # short delay after reading a QR to prevent multiple sends

        cv2.imshow("🎫 Scan your Ticket QR (press Q to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🔴 Exiting scanner.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    read_qr_from_camera()
