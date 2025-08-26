from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule 
import time
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal, TemperatureSensor, AirQualitySensorPM25, LightSensor
from datetime import datetime,timedelta
from pydantic import BaseModel
from sqlalchemy import func

app = FastAPI()


Base.metadata.create_all(bind=engine)

def get_db(): # Dependency to get DB session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TempCreate(BaseModel): # Pydantic model for temperature data
    value: float
    unit: str
    timestamp: datetime

class AirQualityCreate(BaseModel): # Pydantic model for air quality data
    value: float
    unit: str
    timestamp: datetime

class LightCreate(BaseModel): # Pydantic model for light data
    value: float
    unit: str
    timestamp: datetime

@app.post("/data/add_temperature") # Endpoint to add temperature data
def add_temperature(payload: TempCreate, db: Session = Depends(get_db)):
    row = TemperatureSensor(
        value=payload.value,
        unit=payload.unit,
        timestamp=payload.timestamp
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    if row.value > 30: # Alert threshold for temperature
        temp_send_email(row.value, row.unit)
    return {
        "id": row.id,
        "value": row.value,
        "unit": row.unit,
        "timestamp": row.timestamp
    }


@app.post("/data/add_air_quality") #Endpoint to add air quality data
def add_air_quality(payload: AirQualityCreate, db: Session = Depends(get_db)):
    row = AirQualitySensorPM25(
        value=payload.value,
        unit=payload.unit,
        timestamp=payload.timestamp
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    if row.value > 100: # Alert threshold for air quality
        air_send_email(row.value, row.unit)
    return {
        "id": row.id,
        "value": row.value,
        "unit": row.unit,
        "timestamp": row.timestamp
    }

@app.post("/data/add_light") #Endpoint to add light data
def add_light(payload: LightCreate, db: Session = Depends(get_db)):
    row = LightSensor(
        value = payload.value,
        unit = payload.unit,
        timestamp = payload.timestamp
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    if row.value > 800: # Alert threshold for light intensity
        light_send_email(row.value, row.unit)
    return{
        "id": row.id,
        "value": row.value,
        "unit": row.unit,
        "timestamp": row.timestamp
    }

@app.get("/") # Root endpoint
def read_root():
    return {"message": "Welcome to environment sensor data"}

@app.get("/data/latest_temperature") # Endpoint to get latest temperature data
def home_temperature(db: Session = Depends(get_db)):
    row = (
        db.query(TemperatureSensor)
        .order_by(TemperatureSensor.timestamp.desc(), TemperatureSensor.id.desc())
        .first()
    )

    if row is None:
        raise HTTPException(status_code=404, detail="No temperature data found")
    return {
        "temperature": row.value,
        "unit": row.unit,
        "timestamp": row.timestamp
    }


@app.get("/data/latest_air") # Endpoint to get latest air quality data
def home_air_quality(db: Session = Depends(get_db)):
    row = (
        db.query(AirQualitySensorPM25)
        .order_by(AirQualitySensorPM25.timestamp.desc(), AirQualitySensorPM25.id.desc())
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="No air quality data found")
    return {
        "pm2_5": row.value,
        "unit": row.unit,
        "timestamp": row.timestamp
    }
@app.get("/data/latest_light") # Endpoint to get latest light data
def home_light(db: Session = Depends(get_db)):
    row = (
        db.query(LightSensor)
        .order_by(LightSensor.timestamp.desc(), LightSensor.id.desc())
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="No light data found")
    return {
        "light_intensity": row.value,
        "unit": row.unit,
        "timestamp": row.timestamp
    }


@app.get("/key_stats") # Endpoint to get key statistics
def key_stats(db: Session = Depends(get_db)):
    return {
    "temperature_sensor": {
        "total_readings": db.query(TemperatureSensor).count(),
        "latest_reading": db.query(TemperatureSensor).order_by(TemperatureSensor.timestamp.desc(), TemperatureSensor.id.desc()).first().value if db.query(TemperatureSensor).count() > 0 else None,
        "average_reading": db.query(func.avg(TemperatureSensor.value)).scalar() if db.query(TemperatureSensor).count() > 0 else None,
        "Peak_reading": db.query(func.max(TemperatureSensor.value)).scalar() if db.query(TemperatureSensor).count() > 0 else None
    },
    "air_quality_sensor_pm2_5": {
        "total_readings": db.query(AirQualitySensorPM25).count(),
        "latest_reading": db.query(AirQualitySensorPM25).order_by(AirQualitySensorPM25.timestamp.desc(), AirQualitySensorPM25.id.desc()).first().value if db.query(AirQualitySensorPM25).count() > 0 else None,
        "average_reading": db.query(func.avg(AirQualitySensorPM25.value)).scalar() if db.query(AirQualitySensorPM25).count() > 0 else None,
        "Peak_reading": db.query(func.max(AirQualitySensorPM25.value)).scalar() if db.query(AirQualitySensorPM25).count() > 0 else None
    },
    "light_sensor": {
        "total_readings": db.query(LightSensor).count(),
        "latest_reading": db.query(LightSensor).order_by(LightSensor.timestamp.desc(), LightSensor.id.desc()).first().value if db.query(LightSensor).count() > 0 else None,
        "average_reading": db.query(func.avg(LightSensor.value)).scalar() if db.query(LightSensor).count() > 0 else None,
        "Peak_reading": db.query(func.max(LightSensor.value)).scalar() if db.query(LightSensor).count() > 0 else None
    }}

@app.get("/export") # Endpoint to export data
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


def temp_send_email(value, unit): # Function that will send alert email  
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "add_sender_email_here"
    receiver_email = "add_receiver_email_here"
    passwword = "add_own_password_here"


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Environment Sensor Alert System"

    body = "ALERT! Sensor detected value of {} {}".format(value, unit) + " which is above the {} {} threshold.".format(30, "C")
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







def air_send_email(value, unit): # Function that will send alert email  
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "add_sender_email_here"
    receiver_email = "add_receiver_email_here"
    passwword = "add_own_password_here"


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Environment Sensor Alert System"

    body = "ALERT! Sensor detected value of {} {}".format(value, unit) + " which is above the {} {} threshold.".format(100, "µg/m3")
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




def light_send_email(value, unit): # Function that will send alert email  
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "add_sender_email_here"
    receiver_email = "add_receiver_email_here"
    passwword = "add_own_password_here"


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Environment Sensor Alert System"

    body = "ALERT! Sensor detected value of {} {}".format(value, unit) + " which is above the {} {} threshold.".format(800, "lux")
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









