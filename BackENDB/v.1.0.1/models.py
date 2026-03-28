from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from .database import Base

# ORM model representing the "button_presses" table
class StockEntry(Base):
    __tablename__ = "stock_entries"  # Explicit table name in the database

    # Primary key column
    # - Integer auto-incrementing ID
    # - index=True creates a DB index for faster lookups (useful for queries/filtering)
    id = Column(Integer, primary_key=True, index=True)
    
    #This will be for the items type IE a drop down menu on front end shows dress, shirt, pants, skirt, gloves, socks
    item = Column(String)

    #This will be for the colours of the item, ie it will have check mark boxes for these due to possible multiple colours
    colour = Column(String)

    #This will be for the size of the item, ie will be a radio button for the sizes sm, med, large, xl
    size = Column(String)

    #Since its possible the store could get in multiple items of the same attributes need quanitity, will be a text box to input amount
    quantity = Column(Integer)

    #This will have the time stamp of the stock intake
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Timestamp column for when the button was pressed
    # - timezone=True ensures timezone-aware timestamps (important for consistency)
    # - server_default=func.now() lets the DATABASE assign the timestamp (not Python)
    # - nullable=False enforces that every row must have a timestamp
   # pressed_at = Column(
     #   DateTime(timezone=True),
      #  server_default=func.now(),
       # nullable=False
  #  )