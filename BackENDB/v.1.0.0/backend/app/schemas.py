from pydantic import BaseModel
from datetime import datetime

# Response schema for a single button press
# Controls what fields are returned to the client
class ButtonPressResponse(BaseModel):
    id: int                 # Unique identifier of the press
    pressed_at: datetime    # Timestamp of when the press occurred

    class Config:
        # Allows Pydantic to read data directly from ORM objects (SQLAlchemy models)
        # Instead of requiring dicts, it can accept model instances like `ButtonPress`
        from_attributes = True

# Response schema for aggregated count
# Used when returning total number of presses
class ButtonPressCount(BaseModel):
    count: int              # Total number of button presses