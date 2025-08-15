# 🔥 IoT Fire Detection – Backend Module (Nidhi's Contribution)

This module is part of a larger IoT-based Fire Detection and Alerting System. It handles the backend logic for receiving sensor data, evaluating danger thresholds, and sending real-time alerts to the frontend dashboard.

Developed by **Nidhi** as part of Assignment 3 (Code Development Phase).

---

## 📦 Features

- Flask REST API to receive temperature and smoke data  
- Real-time alert broadcasting using Socket.IO  
- Configurable thresholds for triggering fire alerts  
- Basic frontend webpage to display live fire alerts  
## 🚀 How to Run and Use

Make sure Python is installed on your system.

1. **Install dependencies**  
   Open a terminal in the project directory and run:
   ```bash
   pip install -r requirements.txt
   
2. Start the server
   Run the backend server with:python main.py

The Flask server will start at http://localhost:5000.
Navigating to this URL will display a basic frontend webpage (index.html) that listens for real-time fire alerts.

3. Send test data
   You can now test the API using tools like curl or Postman by sending a POST request to send data

If the temperature exceeds 50°C or smoke level is above 300, the server triggers a real-time fire alert using Socket.IO. This alert will be immediately displayed on the frontend webpage.

File Structure: 
1.) Main.py:# Flask server with Socket.IO
2.) requirements.txt     # Dependencies
3.) templates/
    └── index.html       # Frontend alert page
	
To summarize this backend module:

Accepts simulated sensor data via REST

Triggers alerts when thresholds are exceeded

Sends alerts to the browser in real time

Includes unit tests for logic validation

Displays fire alerts on a simple frontend page