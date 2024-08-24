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

#root domain
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

#user id
@app.post("/users/login")
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


@app.get("/users/id/")
def get_user_id_by_name(name: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id}

#user ranking
@app.post("/users/{user_id}/ranking/")
def update_user_ranking(user_id: int, ranking: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.ranking = ranking
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "ranking": user.ranking}


@app.get("/users/{user_id}/ranking/")
def get_user_ranking(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "name": user.name, "ranking": user.ranking}


@app.get("/users/rankings/")
def get_all_user_rankings(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.ranking).all()
    return [{"id": user.id, "name": user.name, "ranking": user.ranking} for user in users]


#user speed
@app.post("/users/{user_id}/speed/")
def update_user_speed(user_id: int, speed: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.speed = speed
    db.commit()
    db.refresh(user)
    return {"id": user.id, "speed": user.speed}


@app.get("/users/{user_id}/speed/")
def get_user_speed(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "speed": user.speed}


#user code add=
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


