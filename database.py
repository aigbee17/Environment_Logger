from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer #necessary import


DATABASE_URL = "sqlite:///./sensor.db" # SQLite database URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


class TemperatureSensor(Base): # Model for temperature sensor data
    __tablename__ = "temperature_sensor"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

class AirQualitySensorPM25(Base): # Model for air quality sensor data
    __tablename__ = "air_quality_sensor_pm2_5"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class LightSensor(Base): # Model for light sensor data
    __tablename__ = "light_sensor"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


Base.metadata.create_all(bind=engine) # Create tables in the database