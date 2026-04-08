#used SQLGREP initially however, I could not get it to run properly with the front end
#I saw in examples that sqlite is much easier to do this connection so had to change

import sqlite3
from pathlib import Path

#Defining the path to sqlite database file
DB_PATH = Path(__file__).parent.parent / "stockapp.db"

def get_db():
    try:
        conn= sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print("Error connecting to database: {e}")
        return None
        