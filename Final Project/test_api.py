import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sensor_data_safe(client):
    response = client.post('/sensor-data', json={
        'temperature': 25,
        'smoke': 100
    })
    assert response.status_code == 200
    assert response.get_json()['status'] == 'safe'

def test_sensor_data_alert(client):
    response = client.post('/sensor-data', json={
        'temperature': 60,
        'smoke': 350
    })
    assert response.status_code == 200
    assert response.get_json()['status'] == 'alert sent'
