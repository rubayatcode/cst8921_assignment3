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

------Rubayat's Contribution-------

This project is a Flask-based web application that simulates an IoT fire detection and alerting system. The system uses simulated IoT sensors to generate temperature and smoke data, stores data in an SQL database, and provides a real-time dashboard for users to monitor fire hazards. Alerts are triggered when thresholds are exceeded.
🚀 Features
Python-based IoT sensor simulator (temperature & smoke).
Flask REST API to collect and process sensor data.
Real-time dashboard (with Socket.IO integration for instant alerts).
SQL database integration (SQLite locally, Azure SQL for cloud deployment).
Event logging for audit trails and analytics.
Modular architecture for easy scalability.
⚙️ Installation & Setup
1. Clone the repository
git clone <repo-url>
cd project-root
2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
3. Install dependencies
pip install -r requirements.txt
4. Initialize the database
python
>>> from app import db
>>> db.create_all()
>>> exit()
This creates tables (users, iot_devices, event_log) in SQLite (fire_alert.db).
For Azure SQL, update the database URI in app.py.
▶️ Running the Application
Start the Flask server:
python app.py
You should see:
 * Running on http://127.0.0.1:5000
📊 Using the Dashboard
Open browser → http://127.0.0.1:5000/login
Login with registered user credentials (create via SQL directly if no signup page yet).
Access dashboard → http://127.0.0.1:5000/dashboard
View live sensor readings and fire alerts.
🔬 Running the Simulator
Start sensor simulator (generates random data and posts to Flask API):
python simulator.py
It will continuously send temperature and smoke values every few seconds.
Data will appear in your dashboard and also get stored in the database.
🛠️ Stopping the App
Stop Flask server → Press CTRL + C in terminal.
Deactivate virtual environment:
deactivate