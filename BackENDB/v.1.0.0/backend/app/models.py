from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from .database import Base

# ORM model representing the "button_presses" table
class ButtonPress(Base):
    __tablename__ = "button_presses"  # Explicit table name in the database

    # Primary key column
    # - Integer auto-incrementing ID
    # - index=True creates a DB index for faster lookups (useful for queries/filtering)
    id = Column(Integer, primary_key=True, index=True)

    # Timestamp column for when the button was pressed
    # - timezone=True ensures timezone-aware timestamps (important for consistency)
    # - server_default=func.now() lets the DATABASE assign the timestamp (not Python)
    # - nullable=False enforces that every row must have a timestamp
    pressed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )