from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to environment sensor data"}

@app.get("/temperature")
def home_temperature():
    return {"temperature": 22.5, "unit": "Celsius", "timestamp": "2025-08-09T12:00:00Z", "device_id": "esp32-001"}