# api_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Stop, Path, Route, Vehicle, Driver, DailyTrip, Deployment
from movi_agent import app_graph, MoviState
from langchain_core.messages import HumanMessage

app = FastAPI(title="Movi Transport API")

# Allow your React frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to SQLite DB
engine = create_engine("sqlite:///movi.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

@app.get("/")
def root():
    return {"message": "Movi API is running 🚀"}

# ---------- STATIC DATA ----------
@app.get("/stops")
def get_stops():
    session = SessionLocal()
    data = session.query(Stop).all()
    session.close()
    return [{"stop_id": s.stop_id, "name": s.name, "latitude": s.latitude, "longitude": s.longitude} for s in data]

@app.get("/paths")
def get_paths():
    session = SessionLocal()
    data = session.query(Path).all()
    session.close()
    return [{"path_id": p.path_id, "path_name": p.path_name, "stops": p.ordered_list_of_stop_ids} for p in data]

@app.get("/routes")
def get_routes():
    session = SessionLocal()
    data = session.query(Route).all()
    session.close()
    return [{
        "route_id": r.route_id,
        "route_display_name": r.route_display_name,
        "shift_time": r.shift_time,
        "status": r.status,
        "start_point": r.start_point,
        "end_point": r.end_point
    } for r in data]

# ---------- DYNAMIC DATA ----------
@app.get("/trips")
def get_trips():
    session = SessionLocal()
    data = session.query(DailyTrip).all()
    session.close()
    return [{
        "trip_id": t.trip_id,
        "display_name": t.display_name,
        "booking_status_percentage": t.booking_status_percentage,
        "live_status": t.live_status
    } for t in data]

@app.get("/vehicles")
def get_vehicles():
    session = SessionLocal()
    data = session.query(Vehicle).all()
    session.close()
    return [{"vehicle_id": v.vehicle_id, "plate": v.license_plate, "type": v.type, "capacity": v.capacity} for v in data]

@app.get("/drivers")
def get_drivers():
    session = SessionLocal()
    data = session.query(Driver).all()
    session.close()
    return [{"driver_id": d.driver_id, "name": d.name, "phone": d.phone_number} for d in data]


@app.post("/ask-movi")
@app.post("/ask-movi")
def ask_movi(payload: dict):
    query = payload.get("message", "")

    # message-based invocation for the graph
    result = app_graph.invoke({"messages": [HumanMessage(content=query)]})

    # extract final reply from message list
    msgs = result.get("messages", [])
    if not msgs:
        return {"response": "No response from Movi."}

    last = msgs[-1]
    response_text = getattr(last, "content", str(last))

    return {"response": response_text}

# http://127.0.0.1:8000/trips
# http://127.0.0.1:8000/routes
# http://127.0.0.1:8000/stops