from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
#Since there can be multiple colours we need an array for it
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base

# ORM model representing the "button_presses" table
class StockEntry(Base):
    __tablename__ = "stock_items"  # Explicit table name in the database

    # Primary key column
    # - Integer auto-incrementing ID
    # - index=True creates a DB index for faster lookups (useful for queries/filtering)
    id = Column(Integer, primary_key=True, index=True)
    
    #Each new variable needs to have its own column 

    #We have to make sure none of these columns can be left empty so we have to set nullable=False on all of the user input variales
    #This will be for the items type IE a drop down menu on front end shows dress, shirt, pants, skirt, gloves, socks
    item_type = Column(String, nullable=False)

    #This will be for the colours of the item, ie it will have check mark boxes for these due to possible multiple colours
    colours = Column(ARRAY(String), nullable=False)

    #This will be for the size of the item, ie will be a radio button for the sizes sm, med, large, xl
    size = Column(String, nullable=False)

    #Since its possible the store could get in multiple items of the same attributes need quanitity, will be a text box to input amount
    #quantity = Column(Integer, nullable=False) may not need quanitiy

    #This will have the timestamp of the stock intake once it is created
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Timestamp column for when the button was pressed
    # - timezone=True ensures timezone-aware timestamps (important for consistency)
    # - server_default=func.now() lets the DATABASE assign the timestamp (not Python)
    # - nullable=False enforces that every row must have a timestamp