from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# This tells python to look for .env in the current working directory
load_dotenv()

db_url = os.getenv("DATABASE_URL")

# Debugging check: If this prints "None", the .env file isn't being read
print(f"DEBUG: Database URL is: {db_url}")

if db_url is None:
    # Fallback for local development if .env fails
    db_url = "mysql+pymysql://root:password@localhost:3306/ivy_db"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()