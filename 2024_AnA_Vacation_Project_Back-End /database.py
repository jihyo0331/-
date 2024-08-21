from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
# Replace 'username', 'password', 'host', 'port' and 'database_name' with actual values
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:jihyo002%40@localhost:3306/tajahakdang"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for getting a session, to be used in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
