from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

# Import database setup and dependency
from .database import Base, engine, get_db

# Import ORM model (represents DB table)
from .models import StockEntry

# Import response schemas (controls API output shape)
from .schemas import StockItemCreate, StockItemResponse, StockItemCount

# Initialize FastAPI application
app = FastAPI(title="STORE STOCK TAKING API")

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

#This posts to the database the stock item object, with its attributes of item_type, colours and size
@app.post("/items", response_model=StockItemResponse)
def create_item(item: StockItemCreate, db: Session = Depends(get_db)):
    #Instantiate new row of the item with its item_type, colours and size
    stock_item= StockEntry(item_type= item.item_type, colours= item.colours, size= item.size)

    #Stage insert of stock_item object into database
    db.add(stock_item)
    
    #Persist the added stock_item object in the database
    db.commit()

    #Refreshing object to get Database generated values of ID and time stamp
    db.refresh(stock_item)

    #Returned object is serialzed according to the schemas file
    return stock_item


#Gets the item objects contained in the database for use by the frontend
@app.get("/items", response_model=list[StockItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(StockEntry).order_by(StockEntry.created_at.desc()).all()

#Gets the amount of items and stores it in count for use by the frontend
@app.get("/items/count", response_model=StockItemCount)
def get_item_count(db: Session = Depends(get_db)):
    count = db.query(func.count(StockEntry.id)).scalar() or 0
    # scalar() returns None if no rows → fallback to 0
    return {"count": count}

#May do other gets like /items/item_type or /items/size or /items/colours. Just using these gets now to see if they work with the frontend at all
