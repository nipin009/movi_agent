from sqlalchemy.orm import sessionmaker
from models import *
from sqlalchemy import create_engine

# Connect to the SQLite database created earlier
engine = create_engine("sqlite:///movi.db")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Print counts and sample data
print("Total Stops:", session.query(Stop).count())
print("Total Paths:", session.query(Path).count())
print("Total Routes:", session.query(Route).count())
print("Total Trips:", session.query(DailyTrip).count())

print("\nSample Route Names:")
for r in session.query(Route).limit(5):
    print("-", r.route_display_name)
