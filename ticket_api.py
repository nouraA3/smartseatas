
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# تحميل قاعدة بيانات التذاكر
ticket_db = pd.read_csv("ticketdata.csv")

# تجهيز الأعمدة المهمة فقط
relevant_columns = [
    'IDENTITY', 'PROGRAM_NAME', 'PLAY_DATE', 'PLAY_TIME',
    'SEAT_REGION_NAME', 'FLOOR_NO', 'SEAT_ROW', 'SEAT_NO', 'TICKET_ENTRANCE_NO'
]
ticket_db = ticket_db[relevant_columns].dropna().drop_duplicates()
ticket_db = ticket_db.rename(columns={
    'IDENTITY': 'ticket_id',
    'PROGRAM_NAME': 'event_name',
    'PLAY_DATE': 'event_date',
    'PLAY_TIME': 'event_time',
    'SEAT_REGION_NAME': 'region',
    'FLOOR_NO': 'floor',
    'SEAT_ROW': 'row',
    'SEAT_NO': 'seat',
    'TICKET_ENTRANCE_NO': 'entrance_no'
})

# دالة محاكاة لفتح المقعد
def unlock_seat(seat_info):
    print(f"🔓 فتح المقعد: Floor {seat_info['floor']}, Row {seat_info['row']}, Seat {seat_info['seat']}")
    return True

@app.route("/verify-ticket", methods=["POST"])
def verify_ticket():
    data = request.get_json()
    ticket_id = data.get('ticket_id')

    match = ticket_db[ticket_db.ticket_id == ticket_id]

    if not match.empty:
        seat_info = match.iloc[0][['region', 'floor', 'row', 'seat']]
        unlock_result = unlock_seat(seat_info)
        return jsonify({
            "status": "valid",
            "message": "تم التحقق من التذكرة وتم فتح المقعد.",
            "seat_opened": unlock_result
        })
    else:
        return jsonify({
            "status": "invalid",
            "message": "تذكرة غير صالحة.",
            "seat_opened": False
        }), 404

if __name__ == "__main__":
    app.run(debug=True)
