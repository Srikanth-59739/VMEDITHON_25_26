# tests/test_api.py
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Diabetes Prediction API is running!"}

def test_predict():
    # Example patient data
    payload = {
        "Pregnancies": 2,
        "Glucose": 130,
        "BloodPressure": 70,
        "SkinThickness": 20,
        "Insulin": 85,
        "BMI": 28.5,
        "DiabetesPedigreeFunction": 0.45,
        "Age": 35
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    result = response.json()

    # Check response structure
    assert "prediction" in result
    assert result["prediction"] in [0, 1]
    assert "probability_diabetes" in result
    assert 0.0 <= result["probability_diabetes"] <= 1.0
