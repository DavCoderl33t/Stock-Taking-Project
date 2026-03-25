from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import Base, engine, get_db
from .models import ButtonPress
from .schemas import ButtonPressResponse, ButtonPressCount

app = FastAPI(title="Button Press API")

app.add_middleware(
	CORSMiddleware,
	allow_origins["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
	return {"status":"ok"}

@app.post("/presses", response model=ButtonPressResponse)
def create_press(db:Session= Depends(get_db)):
	press = ButtonPress()
	db.add(press)
	db.commit()
	db.refresh(press)
	return press

@app.get("/presses.count", response_model=ButtonPressCount)
def get_press_count(db: Session = Depends(get_db)):
	count = db.query(func.count(ButtonPress.id)).scalar() or 0
	return ("count":count)