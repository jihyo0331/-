from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import database
import pymysql

app = FastAPI()

# Ensure the tables are created
models.Base.metadata.create_all(bind=database.engine)

# Dependency for getting the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/users/")
def create_user(name: str, password: str, db: Session = Depends(get_db)):
    user = models.User(name=name, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/codes/")
def create_code(language: str, code: str, owner_id: int, db: Session = Depends(get_db)):
    code = models.Code(language=language, code=code, owner_id=owner_id)
    db.add(code)
    db.commit()
    db.refresh(code)
    return code

@app.get("/codes/{code_id}")
def read_code(code_id: int, db: Session = Depends(get_db)):
    code = db.query(models.Code).filter(models.Code.id == code_id).first()
    if code is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return code
