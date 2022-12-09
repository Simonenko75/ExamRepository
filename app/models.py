from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from app.config import DATABASE_URL


Base = declarative_base()


def connect_db():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    session = Session(bind=engine.connect())
    return session


class SensorValue(Base):
    __tablename__ = "sensors_values"

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    created_at = Column(String, default=datetime.utcnow())


class SensorName(Base):
    __tablename__ = "sensors_names"

    id = Column(Integer, primary_key=True)
    name_sensor = Column(String)
    user_id = Column(Integer, ForeignKey("sensors_values.id"))