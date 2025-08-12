from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to environment sensor data"}

@app.get("/data/latest_temperature")
def home_temperature():
    return {"temperature": 22.5, "unit": "Celsius", "timestamp": "2025-08-09T12:00:00Z", "device_id": "esp32-001"}


@app.get("/data/latest_air")
def home_air_quality():
    return {"air_quality": "Good", "pm2_5": 12, "pm10": 20, "timestamp": "2025-08-09T12:00:00Z", "device_id": "esp32-001"}

@app.get("/data/latest_light")
def home_light():
    return {"light_intensity": 300, "unit": "lux", "timestamp": "2025-08-09T12:00:00Z", "device_id": "esp32-001"}


@app.get("/key_stats")
def key_stats():
    return {
    "temperature_sensor": {
        "average": {
            "value": 21.8,
            "timestamp": "2025-08-12T01:12:00"
        },
        "peak": {
            "value": 26.13,
            "timestamp": "2025-08-12T00:45:00"
        },
        "min": {
            "value": 18.92,
            "timestamp": "2025-08-12T00:10:00"
        }
    },
    "air_quality_sensor_pm2_5": {
        "average": {
            "value": 15,
            "timestamp": "2025-08-12T01:32:00"
        },
        "peak": {
            "value": 21.84,
            "timestamp": "2025-08-12T00:50:00"
        },
        "min": {
            "value": 13.12,
            "timestamp": "2025-08-12T00:20:00"
        }
    },
    "light_sensor": {
        "average": {
            "value": 250,
            "timestamp": "2025-08-12T01:05:00"
        },
        "peak": {
            "value": 383.65,
            "timestamp": "2025-08-12T00:40:00"
        },
        "min": {
            "value": 191.27,
            "timestamp": "2025-08-12T00:15:00"
        }
    }
}