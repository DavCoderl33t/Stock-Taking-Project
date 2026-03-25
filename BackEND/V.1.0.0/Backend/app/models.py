from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from .database import Base

class ButtonPress(Base):
	__tablename__ = "button_presses"

	id = Column(Integer, primary_key=True, Index=true)
	pressed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)