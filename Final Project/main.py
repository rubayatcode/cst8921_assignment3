import os
from flask import Flask, request, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from datetime import datetime
from functools import wraps
from flask import render_template
import threading
import time

TempMax = 50
SmokeMax = 300

fireDrill_mode = False
offline_timeout = 300

sensor_last_seen = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///fire_alert.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# --- Initialize Extensions ---
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")


# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), default='User')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    smoke_level = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String, nullable=False)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float)
    smoke_level = db.Column(db.Float)
    timestamp = db.Column(db.String)
    severity = db.Column(db.String)
    notification_triggered = db.Column(db.Boolean, default=False)


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == 'user' and password == 'user123':
        return render_template('dashboard.html')
    elif username == 'admin' and password == 'admin123':
        return render_template('admin.html')
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route("/admin")
def admin_panel():
    return render_template('admin.html')


def monitor_sensor_activity():
    while True:
        now = datetime.now()
        for device_id, last_seen in list(sensor_last_seen.items()):
            elapsed = (now - last_seen).total_seconds()
            if elapsed > offline_timeout:
                socketio.emit('device_offline', {"device_id": device_id})
        time.sleep(60)


def handle_sensor_alert(device_id, temperature, smoke_level):
    timestamp = datetime.now().isoformat()

    sensor_last_seen[device_id] = datetime.now()

    alert_data = {
        'device_id': device_id,
        'temperature': temperature,
        'smoke_level': smoke_level,
        'timestamp': timestamp,
        'fire_drill': fireDrill_mode
    }

    if temperature > TempMax or smoke_level > SmokeMax:
        if fireDrill_mode:
            socketio.emit('fire_drill_alert', alert_data)
            print(f"Fire Drill Alert for {device_id} (NOT real).")
        else:
            socketio.emit('fire_alert', alert_data)
            print(f"REAL ALERT: Dispatching 911 for {device_id}!")
    else:
        socketio.emit('sensor_update', alert_data)


@app.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    device_id = data.get('device_id')
    temperature = data.get('temperature')
    smoke_level = data.get('smoke_level')
    timestamp = datetime.now().isoformat()

     # Save to SensorData
    sensor_record = SensorData(
        device_id=device_id,
        temperature=temperature,
        smoke_level=smoke_level,
        timestamp=timestamp
    )
    db.session.add(sensor_record)
    if temperature is None or smoke_level is None:
        return jsonify({'error': 'Missing data'}), 400

    handle_sensor_alert(device_id, temperature, smoke_level)

    alert_triggered = temperature > TempMax or smoke_level > SmokeMax
    severity = "high" if alert_triggered else "low"

    if alert_triggered:
        alert = Alert(
            device_id=device_id,
            temperature=temperature,
            smoke_level=smoke_level,
            timestamp=timestamp,
            severity=severity,
            notification_triggered=True
        )
        db.session.add(alert)
        socketio.emit("fire_alert", {
            "device_id": device_id,
            "temperature": temperature,
            "smoke_level": smoke_level,
            "timestamp": timestamp,
            "alert": True,
            "severity": severity
        })
    else:
        socketio.emit("sensor_update", {
            "device_id": device_id,
            "temperature": temperature,
            "smoke_level": smoke_level,
            "timestamp": timestamp,
            "alert": False
        })

    db.session.commit()
    return jsonify({"status": "received"}), 200

@app.route('/data')
def get_data():
    entries = SensorData.query.order_by(SensorData.timestamp.desc()).limit(10).all()
    return jsonify([
        {
            'device_id': e.device_id,
            'temperature': e.temperature,
            'smoke_level': e.smoke_level,
            'timestamp': e.timestamp
        }
        for e in entries
    ])


@app.route("/init-db")
def init_db():
    db.create_all()
    return "Database tables created successfully."

# Mock login/logout for demo purposes
@app.route("/mock-login/<username>")
def mock_login(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found", 404
    session["user_id"] = user.id
    session["role"] = user.role
    return f"Logged in as {username}"

@app.route("/logout")
def logout():
    session.clear()
    return "Logged out"


if __name__ == '__main__':
    threading.Thread(target=monitor_sensor_activity, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
