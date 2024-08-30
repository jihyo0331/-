from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import get_db
from services.user_service import get_password_hash, verify_password

router = APIRouter()


@router.post("/signup")
def create_user(name: str, password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    user = User(name=name, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name}


@router.post("/login")
def login_user(name: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}


@router.get("/id/")
def get_user_id_by_name(name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id}


@router.post("/{user_id}/ranking/")
def update_user_ranking(user_id: int, ranking: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.ranking = ranking
    db.commit()
    db.refresh(user)
    return {"id": user.id, "ranking": user.ranking}


@router.get("/{user_id}/ranking/")
def get_user_ranking(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "ranking": user.ranking}


@router.post("/{user_id}/speed/")
def update_user_speed(user_id: int, speed: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.speed = speed
    db.commit()
    db.refresh(user)
    return {"id": user.id, "speed": user.speed}


@router.get("/{user_id}/speed/")
def get_user_speed(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "speed": user.speed}


@router.get("/rankings/")
def get_all_user_rankings(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.ranking).all()
    return [{"id": user.id, "name": user.name, "ranking": user.ranking} for user in users]

