# populate_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Stop, Path, Route, Vehicle, Driver, DailyTrip, Deployment
import random

engine = create_engine("sqlite:///movi.db")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # ---------- 1. Stops ----------
    stop_names = [
        "Gavipuram", "Peenya", "Majestic", "Indiranagar", "Koramangala",
        "Electronic City", "Whitefield", "Yeshwanthpur", "BTM Layout", "Hebbal"
    ]
    stops = [Stop(name=n, latitude=12.9 + random.random()/10, longitude=77.5 + random.random()/10)
             for n in stop_names]
    session.add_all(stops)
    session.commit()

    # ---------- 2. Paths ----------
    paths = []
    for i in range(1, 6):  # 5 paths
        stop_ids = random.sample(range(1, len(stops)+1), k=5)
        paths.append(Path(path_name=f"Path-{i}", ordered_list_of_stop_ids=stop_ids))
    session.add_all(paths)
    session.commit()

    # ---------- 3. Routes ----------
    routes = []
    shift_times = ["06:00", "08:00", "10:00", "14:00", "18:00", "20:00"]
    directions = ["Up", "Down"]
    for i in range(1, 6):
        for shift in random.sample(shift_times, 2):
            start = stop_names[random.randint(0, 4)]
            end = stop_names[random.randint(5, 9)]
            routes.append(Route(
                path_id=i,
                route_display_name=f"Path-{i} - {shift}",
                shift_time=shift,
                direction=random.choice(directions),
                start_point=start,
                end_point=end,
                status=random.choice(["active", "deactivated"])
            ))
    session.add_all(routes)
    session.commit()

    # ---------- 4. Vehicles ----------
    vehicles = []
    types = ["Bus", "Cab"]
    for i in range(1, 11):
        vehicles.append(Vehicle(
            license_plate=f"KA-05-{1000+i}",
            type=random.choice(types),
            capacity=random.choice([4, 6, 20, 30, 40])
        ))
    session.add_all(vehicles)
    session.commit()

    # ---------- 5. Drivers ----------
    drivers = []
    driver_names = [
        "Amit", "Ravi", "Suresh", "Deepak", "Vijay",
        "Naveen", "Prakash", "Rohan", "Anil", "Manoj"
    ]
    for i, name in enumerate(driver_names):
        drivers.append(Driver(name=name, phone_number=f"98{random.randint(10000000,99999999)}"))
    session.add_all(drivers)
    session.commit()

    # ---------- 6. DailyTrips ----------
    daily_trips = []
    for i, route in enumerate(session.query(Route).all(), start=1):
        daily_trips.append(DailyTrip(
            route_id=route.route_id,
            display_name=f"Trip-{i:02d}",
            booking_status_percentage=random.choice([0, 10, 25, 50, 75, 100]),
            live_status=random.choice(["Not Started", "IN", "Completed"])
        ))
    session.add_all(daily_trips)
    session.commit()

    # ---------- 7. Deployments ----------
    deployments = []
    trip_ids = [t.trip_id for t in session.query(DailyTrip).all()]
    for trip_id in trip_ids:
        deployments.append(Deployment(
            trip_id=trip_id,
            vehicle_id=random.randint(1, len(vehicles)),
            driver_id=random.randint(1, len(drivers))
        ))
    session.add_all(deployments)
    session.commit()

    print("✅ Database populated successfully!")

except Exception as e:
    print("❌ Error:", e)

finally:
    session.close()
