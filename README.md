# smartseatas
🎟️ Smart Stadium Ticket Verification System

💡 Project Overview:

"Makani" is an AI-powered smart ticket verification system designed for stadium seats. Each seat is equipped with a QR scanner and sensors, and the system uses machine learning to validate tickets and control seat access — ensuring a smooth, secure, and automated fan experience.

⚙️ Key Features:

🎫 Smart seats that only open once the correct QR ticket is scanned.
🤖 AI model trained to detect fraudulent or invalid tickets.
📡 Integration with mobile apps (such as Tawakkalna) to guide fans directly to their seats.
💡 Seat occupancy detection via sensors — seats close automatically if left unused.
📊 Real-time analytics for event organizers to monitor attendance and seat status.
🧠 AI Implementation:

Using a RandomForestClassifier trained on real and synthetic ticket data.
The model predicts whether a scanned ticket is valid or fake based on historical patterns.
Achieved training accuracy:
✅ Ticket validity model accuracy: ~83%  (after fixing data imbalance & adding label simulation)
The system is designed to self-improve as more ticket data is collected.
🧪 Live Testing:

A Python client opens the webcam, scans the QR code, and sends it to the Flask verification API. Based on the server’s AI prediction, the system either:

✅ Unlocks the seat for valid tickets.
❌ Rejects invalid or mismatched ones.
💡 Technologies Used:

Python / Flask
Scikit-learn (AI Model: Random Forest Classifier)
OpenCV + Pyzbar (QR Code scanning)
JSON-based API communication
Real-time seat management logic
🚀 Future Roadmap:

Integrate face recognition for advanced verification.
Predict crowd flow & optimize entry paths using AI.
Expand system coverage beyond stadiums: theaters, concerts, conferences.
💡 This system merges physical security with artificial intelligence to create a safer and smarter stadium experience.

