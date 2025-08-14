from fastapi import FastAPI
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule 
import time

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

@app.get("/export")
def export_data():
    return {
        "exported_data": [
            {
                "device_id": "esp32-001",
                "timestamp": "2025-08-09T12:00:00Z",
                "temperature": 22.5,
                "air_quality": {
                    "pm2_5": 12,
                    "pm10": 20,
                    "quality": "Good"
                },
                "light_intensity": 300
            }
        ]
    }

def send_email():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "add_sender_email_here"
    receiver_email = "add_receiver_email_here"
    passwword = "add_own_password_here"


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Environment Sensor Data Export"

    body = "Please find the attached exported data."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, passwword)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")


schedule.every(1).minutes.do(send_email)

while True:
        schedule.run_pending()
        time.sleep(10)