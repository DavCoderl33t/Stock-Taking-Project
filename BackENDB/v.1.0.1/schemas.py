from pydantic import BaseModel
from datetime import datetime

# The request schema data comming from front end
class StockCreate(BaseModel):
    #this is the item type from front end
    item: str

    #this is the colour coming from the front end
    colour: str

    #this is the size comning from the front end
    size: str

    #this is the quanitity coming from the front end
    quantity: int


# The response Schema used when sending a stock entry to show up in the frontend
class StockResponse(BaseModel):
    
    # The id that was set when it was sent to the database
    id: int

    #The item, colour, size and quanity values sent to the front end
    item: str
    colour: str
    size: str
    quantity: int

    class Config:
        # Allows Pydantic to read data directly from ORM objects (SQLAlchemy models)
        # Instead of requiring dicts, it can accept model instances like `ButtonPress`
        from_attributes = True
