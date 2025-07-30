IoT Fire Detection – Backend Module (Nidhi's Contribution)

This module is part of a larger IoT-based Fire Detection and Alerting System. It handles the backend logic for receiving sensor data, checking danger thresholds, and sending real-time alerts.


Features:

- Flask REST API to receive temperature and smoke data
- Real-time alert broadcasting using Socket.IO
- Configurable thresholds for triggering fire alerts
- Unit tests using Pytest to verify logic and responses

How to Run & Use:

Step 1: Install Dependencies
Make sure you have Python installed. Open a terminal in the project folder and run:
pip install -r requirements.txt

Once dependencies are installed, start the backend server using:
python main.py

The server will start at:
http://localhost:5000

Now, test the API by sending a POST request to /sensor-data using a tool like Postman or curl. Your request should look like:

{
  "temperature": 60,
  "smoke": 350
}

If values exceed the defined thresholds (temperature > 50°C or smoke > 300), the server will return:

{
  "status": "alert sent",
  "data": { "temperature": 60, "smoke": 350 }
}

Otherwise, it will return:

{
  "status": "safe",
  "data": { "temperature": 25, "smoke": 100 }
}

Additionally, when an alert is triggered, the server emits a fire_alert event using Socket.IO, which can be captured by the frontend in real time.

To verify functionality, run the unit tests:
pytest test_api.py

This will validate the core logic and responses of the backend API.

File Overview:

main.py          - Core Flask app with alert logic
test_api.py      - Pytest file for backend API tests
requirements.txt - Python dependencies list
README.txt       - Project documentation (this file)

From Rubayat For Database implementation and sotring information 

Create a virtual environment -

python3 -m venv path/to/venv

source path/to/venv/bin/activate

Install required packages -

python3 -m pip install flask flask-socketio requests flask_sqlalchemy python-dotenv 

Run the Flask app -

python3 app.py     


Run the simulator file to generate data

python3 sensor_simulator.py


Access the url in browser to check the generated data

http://127.0.0.1:5001




