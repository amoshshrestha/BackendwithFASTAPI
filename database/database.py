from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update the connection URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:adminamosh@localhost:5432/Childcare"

# Create the engine for PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configure the session
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

