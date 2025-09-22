from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database_schema import Base
import os

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///sports_betting.db')

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

# Get database session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
