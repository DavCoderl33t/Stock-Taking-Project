from pydantic import BaseModel, Field, field_validator
from datetime import datetime

#Since I read that frontend options are not enough to limit actual options sent to backend
#Will do verification of the fields to make sure the backend does not recieve invalid inputs from malicious actors

ALL_ITEM_TYPES = {"Pants", "Shirt", "Dress","Socks"}
ALL_SIZES = {"Small", "Medium", "Large", "XLarge"}
ALL_COLOURS = {"Blue", "Black", "White", "Yellow", "Red", "Grey", "Brown", "Green", "Pink"}


# The request schema data comming from frontend
class StockItemCreate(BaseModel):
    #this is the item type from frontend
    item_type: str

    #this is the colour coming from the frontend, and ensures that there is atleast one colour in the array
    colours: list[str] = Field(min_length = 1)

    #this is the size comning from the frontend
    size: str

    #this is the quanitity coming from the frontend
    #quantity: int

    #Field validator for item_type, if it isn't part of the frontend options then raise an error
    @field_validator("item_type")
    @classmethod
    def validate_item_type(cls, value: str) -> str:
        if value not in ALL_ITEM_TYPES:
            raise ValueError("Invalid item type")
        return value

    #Field validator for size
    @field_validator("size")
    @classmethod
    def validate_size(cls, value: str) -> str:
        if value not in ALL_SIZES:
            raise ValueError("Invalid Size")
        return value

    #Field validator for colours
    @field_validator("colours")
    @classmethod
    def validate_colours(cls, value: list[str]) -> list[str]:
        for colours in value:
            if colours not in ALL_COLOURS:
                raise ValueError("Invalid Colour")
        return value

# The response Schema used when sending a stock entry to show up in the frontend
class StockItemResponse(BaseModel):
    
    # The id that was set when it was sent to the database
    id: int

    #The item_type, colours, size and created_at values sent to the front end
    item_type: str
    colours: list[str]
    size: str
    created_at: datetime

    class Config:
        # Allows Pydantic to read data directly from ORM objects (SQLAlchemy models)
        # Instead of requiring dicts, it can accept model instances like `ButtonPress`
        from_attributes = True

#counts the items in the stock to ensure all were entered
class StockItemCount(BaseModel):
    count: int
