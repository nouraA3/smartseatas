from flask import Flask, request, jsonify
import pandas as pd
import json
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# Load ticket database
ticket_db = pd.read_csv("ticketdata.csv")

# Select relevant columns
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

# Add a simulated 'valid' label for AI training (1: valid, 0: invalid)
ticket_db['valid'] = 1  # Mark all real tickets as valid

# Duplicate and create some fake (invalid) samples for training
ticket_db_invalid = ticket_db.sample(frac=0.3).copy()
ticket_db_invalid['valid'] = 0

# Inject wrong data to simulate fake tickets
ticket_db_invalid['seat'] = ticket_db_invalid['seat'].sample(frac=1).values

# Combine real and fake tickets for training
dataset = pd.concat([ticket_db, ticket_db_invalid], ignore_index=True)

# Encode categorical data
dataset_encoded = dataset.copy()
dataset_encoded['event_name'] = dataset_encoded['event_name'].astype('category').cat.codes
dataset_encoded['event_date'] = dataset_encoded['event_date'].astype('category').cat.codes
dataset_encoded['event_time'] = dataset_encoded['event_time'].astype('category').cat.codes
dataset_encoded['region'] = dataset_encoded['region'].astype('category').cat.codes
dataset_encoded['ticket_id'] = dataset_encoded['ticket_id'].astype('category').cat.codes

# Prepare data for model
X = dataset_encoded.drop(['valid'], axis=1)
y = dataset_encoded['valid']  # Predict validity, not ticket_id

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Ticket validity model accuracy: {accuracy * 100:.2f}%")

# Seat unlocking simulation function
def unlock_seat(seat_info):
    print(f"🔓 Seat unlocked: Floor {seat_info['floor']}, Row {seat_info['row']}, Seat {seat_info['seat']}")
    return True

@app.route("/verify-ticket", methods=["POST"])
def verify_ticket():
    data = request.get_json()

    # Check ticket validity against real database
    match = ticket_db[
        (ticket_db.ticket_id == data['ticket_id']) &
        (ticket_db.event_name == data['event_name']) &
        (ticket_db.event_date == data['event_date']) &
        (ticket_db.event_time == data['event_time']) &
        (ticket_db.region == data['seat_location']['region']) &
        (ticket_db.floor == data['seat_location']['floor']) &
        (ticket_db.row == data['seat_location']['row']) &
        (ticket_db.seat == data['seat_location']['seat'])
    ]

    if not match.empty:
        unlock_result = unlock_seat(data['seat_location'])
        return jsonify({
            "status": "valid",
            "message": "Ticket verified and seat unlocked.",
            "seat_opened": unlock_result
        })
    else:
        return jsonify({
            "status": "invalid",
            "message": "Invalid ticket or seat mismatch.",
            "seat_opened": False
        }), 404

if __name__ == "__main__":
    app.run(debug=True)
