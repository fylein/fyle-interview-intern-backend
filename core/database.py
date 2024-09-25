from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a new SQLAlchemy engine instance (adjust the connection URL as per your setup)
engine = create_engine('sqlite:///example.db')  # Use your actual database URL

# Create a declarative base class
Base = declarative_base()

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session for requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
