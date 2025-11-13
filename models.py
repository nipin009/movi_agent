# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import JSON

Base = declarative_base()

class Stop(Base):
    __tablename__ = "stops"
    stop_id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

class Path(Base):
    __tablename__ = "paths"
    path_id = Column(Integer, primary_key=True)
    path_name = Column(String)
    ordered_list_of_stop_ids = Column(JSON)

class Route(Base):
    __tablename__ = "routes"
    route_id = Column(Integer, primary_key=True)
    path_id = Column(Integer, ForeignKey("paths.path_id"))
    route_display_name = Column(String)
    shift_time = Column(String)
    direction = Column(String)
    start_point = Column(String)
    end_point = Column(String)
    status = Column(String)

class Vehicle(Base):
    __tablename__ = "vehicles"
    vehicle_id = Column(Integer, primary_key=True)
    license_plate = Column(String)
    type = Column(String)
    capacity = Column(Integer)

class Driver(Base):
    __tablename__ = "drivers"
    driver_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)

class DailyTrip(Base):
    __tablename__ = "daily_trips"
    trip_id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.route_id"))
    display_name = Column(String)
    booking_status_percentage = Column(Integer)
    live_status = Column(String)

class Deployment(Base):
    __tablename__ = "deployments"
    deployment_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("daily_trips.trip_id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id"))
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
