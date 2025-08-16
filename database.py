from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer 


DATABASE_URL = "sqlite:///./sensor.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


class TemperatureSensor(Base):
    __tablename__ = "temperature_sensor"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

class AirQualitySensorPM25(Base):
    __tablename__ = "air_quality_sensor_pm2_5"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class LightSensor(Base):
    __tablename__ = "light_sensor"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


Base.metadata.create_all(bind=engine)