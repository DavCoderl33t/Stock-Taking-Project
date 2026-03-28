import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read the database connection string from environment variables
# Example: postgresql://user:password@host:port/dbname
DATABASE_URL = os.environ["DATABASE_URL"]

# Create the SQLAlchemy engine (core interface to the database)
# This manages connections and communicates with the DB backend
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
# - autocommit=False: changes must be explicitly committed
# - autoflush=False: prevents automatic syncing to DB before queries
# - bind=engine: attaches this session to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
# All database table models will inherit from this
Base = declarative_base()

def get_db():
    """
    Dependency function (commonly used with FastAPI)

    Provides a database session to request handlers:
    - Opens a new session
    - Yields it for use
    - Ensures it is properly closed after request completes

    This pattern prevents connection leaks and ensures clean lifecycle management.
    """
    db = SessionLocal()  # Create a new database session
    try:
        yield db          # Provide the session to the caller (e.g., API route)
    finally:
        db.close()        # Always close the session after use