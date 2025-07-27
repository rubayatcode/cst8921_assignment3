import os
from flask import Flask, request, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from datetime import datetime
from functools import wraps

# --- Setup Flask App ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///fire_alert.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Initialize Extensions ---
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Alert Thresholds ---
ALERT_TEMP_THRESHOLD = 60
ALERT_SMOKE_THRESHOLD = 80

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

# --- Decorators ---
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return abort(401, description="Login required.")
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "Admin":
            return abort(403)
        return f(*args, **kwargs)
    return wrapper

# --- Routes ---

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome {session['user_id']} (Role: {session['role']})"

@app.route("/admin")
@admin_required
def admin_panel():
    return "Admin Control Panel - Secure Area"

@app.route("/sensor-data", methods=["POST"])
def sensor_data():
    data = request.get_json()
    device_id = data.get("device_id")
    temp = data.get("temperature")
    smoke = data.get("smoke_level")
    timestamp = datetime.now().isoformat()

    # Save to SensorData
    sensor_record = SensorData(
        device_id=device_id,
        temperature=temp,
        smoke_level=smoke,
        timestamp=timestamp
    )
    db.session.add(sensor_record)

    alert_triggered = temp > ALERT_TEMP_THRESHOLD or smoke > ALERT_SMOKE_THRESHOLD
    severity = "high" if alert_triggered else "low"

    if alert_triggered:
        alert = Alert(
            device_id=device_id,
            temperature=temp,
            smoke_level=smoke,
            timestamp=timestamp,
            severity=severity,
            notification_triggered=True
        )
        db.session.add(alert)
        socketio.emit("fire_alert", {
            "device_id": device_id,
            "temperature": temp,
            "smoke_level": smoke,
            "timestamp": timestamp,
            "alert": True,
            "severity": severity
        })
    else:
        socketio.emit("sensor_update", {
            "device_id": device_id,
            "temperature": temp,
            "smoke_level": smoke,
            "timestamp": timestamp,
            "alert": False
        })

    db.session.commit()
    return jsonify({"status": "received"}), 200

@app.route("/alerts")
@login_required
def get_alerts():
    results = Alert.query.order_by(Alert.timestamp.desc()).limit(10).all()
    return jsonify([
        {
            "device_id": a.device_id,
            "temperature": a.temperature,
            "smoke_level": a.smoke_level,
            "timestamp": a.timestamp,
            "severity": a.severity
        } for a in results
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

# --- Run the App ---
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)
