from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#To help with the colour variable issues 
import json

#had to remove sql alchemy and other grep stuff to make way for sqlite3
import sqlite3
from contextlib import contextmanager
from pathlib import Path


# Import database setup and dependency
#from .database import Base, engine, get_db

# Import ORM model (represents DB table)
#from .models import StockEntry

# Import response schemas (controls API output shape)
from src.schemas import StockItemCreate, StockItemResponse, StockItemCount

#Setting Database file Path
DB_PATH = Path(__file__).parent.parent / "stockapp.db"


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


#Database connection help
@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    
    #Allows for returning rows as dictionaries
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()

#Initialization of Table which is similar to the Base.metadata.create_all previously used
def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stock_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_type TEXT NOT NULL,
                colours TEXT NOT NULL,
                size TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

init_db()

@app.get("/")
def health_check():
    return {"status": "ok"}

#This posts to the database the stock item object, with its attributes of item_type, colours and size
@app.post("/items", response_model=StockItemResponse)
def create_item(item: StockItemCreate):
    with get_db() as conn:
        cursor= conn.cursor()
        
        #inserting the data
        query= "INSERT INTO stock_entries (item_type, colours, size) VALUES (?, ?, ?)"
        cursor.execute(query, (item.item_type, json.dumps(item.colours), item.size))
        
        #commits the transaction to the database
        conn.commit()

        #Fetching the new item to return
        last_id= cursor.lastrowid
        cursor.execute("SELECT * FROM stock_entries WHERE id = ?", (last_id,))
        
        #Getting the row from SQLite 
        new_item= cursor.fetchone()

        #now turning the item into a normal dictionary
        new_item= dict(new_item)

        #changing to list
        new_item["colours"]= json.loads(new_item["colours"])

        return new_item


#Gets the item objects contained in the database for use by the frontend
@app.get("/items", response_model=list[StockItemResponse])
def get_items():
    with get_db() as conn:
        cursor= conn.cursor()
        cursor.execute("SELECT * FROM stock_entries ORDER BY created_at DESC")
        rows= cursor.fetchall()

        #convert each sqlite row into a normal dictionary and turn colours back into a list
        items= []
        for row in rows:
            item= dict(row)
            item["colours"]= json.loads(item["colours"])
            items.append(item)
        return items

#Gets the amount of items and stores it in count for use by the frontend
@app.get("/items/count", response_model=StockItemCount)
def get_item_count():
    with get_db() as conn:
        cursor= conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM stock_entries")
        count= cursor.fetchone()[0]
        return {"count": count}