from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

# Import database setup and dependency
from .database import Base, engine, get_db

# Import ORM model (represents DB table)
from .models import ButtonPress

# Import response schemas (controls API output shape)
from .schemas import ButtonPressResponse, ButtonPressCount

# Initialize FastAPI application
app = FastAPI(title="Button Press API")

# Enable CORS (Cross-Origin Resource Sharing)
# Allows frontend apps (even on different domains) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins (open; tighten in production)
    allow_credentials=True,
    allow_methods=["*"],        # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"]         # Allow all headers
)

# Create database tables based on ORM models
# Runs at startup if tables do not already exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    """
    Simple health check endpoint
    Useful for:
    - Load balancers
    - Container health probes
    - Quick manual checks
    """
    return {"status": "ok"}

@app.post("/presses", response_model=ButtonPressResponse)
def create_press(db: Session = Depends(get_db)):
    """
    Create a new button press record

    Flow:
    1. Create ORM object
    2. Add to session
    3. Commit transaction (writes to DB)
    4. Refresh to get DB-generated values (e.g., ID, timestamp)
    """
    press = ButtonPress()   # Instantiate new row
    db.add(press)           # Stage insert
    db.commit()             # Persist to database
    db.refresh(press)       # Reload object with DB values
    return press            # Returned object is serialized via schema

@app.get("/presses/count", response_model=ButtonPressCount)
def get_press_count(db: Session = Depends(get_db)):
    """
    Get total number of button presses

    Uses SQL COUNT aggregation for efficiency (no full row fetch)
    """
    count = db.query(func.count(ButtonPress.id)).scalar() or 0
    # scalar() returns None if no rows → fallback to 0
    return {"count": count}