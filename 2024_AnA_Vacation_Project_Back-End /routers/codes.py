from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Code
from database import get_db

router = APIRouter()

@router.post("/")
def create_code(language: str, code: str, owner_id: int, db: Session = Depends(get_db)):
    code_entry = Code(language=language, code=code, owner_id=owner_id)
    db.add(code_entry)
    db.commit()
    db.refresh(code_entry)
    return code_entry

@router.get("/{code_id}")
def read_code(code_id: int, db: Session = Depends(get_db)):
    code = db.query(Code).filter(Code.id == code_id).first()
    if not code:
        raise HTTPException(status_code=404, detail="Code not found")
    return code
