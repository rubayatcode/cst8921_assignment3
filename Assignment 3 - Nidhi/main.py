from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

# Threshold config (previously in config.py)
TEMP_THRESHOLD = 50  # degrees Celsius
SMOKE_THRESHOLD = 300  # arbitrary smoke level

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    temperature = data.get('temperature')
    smoke_level = data.get('smoke')

    if temperature is None or smoke_level is None:
        return jsonify({'error': 'Missing data'}), 400

    if temperature > TEMP_THRESHOLD or smoke_level > SMOKE_THRESHOLD:
        alert = {'temperature': temperature, 'smoke': smoke_level}
        socketio.emit('fire_alert', alert)
        return jsonify({'status': 'alert sent', 'data': alert}), 200

    return jsonify({'status': 'safe', 'data': data}), 200

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
