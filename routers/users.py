from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User as UserModel, Segment, UserSegment
from schemas import User, UserCreate, UserSegmentCreate
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(
        id=db_user.id,
        name=db_user.name,
        segments=[],
    )


@router.get("/", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    segment_names = [rel.segment.name for rel in user.segments]
    return User(id=user.id, name=user.name, segments=segment_names)


@router.get("/{user_id}/segments", response_model=List[str])
def get_user_segments(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [rel.segment.name for rel in user.segments]


@router.post("/assign/")
def assign_user_to_segment(data: UserSegmentCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == data.user_id).first()
    segment = db.query(Segment).filter(Segment.id == data.segment_id).first()
    if not user or not segment:
        raise HTTPException(status_code=404, detail="User or Segment not found")

    # Проверим, нет ли уже такой связи
    existing = db.query(UserSegment).filter_by(
        user_id=data.user_id, segment_id=data.segment_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Relation already exists")

    relation = UserSegment(user_id=data.user_id, segment_id=data.segment_id)
    db.add(relation)
    db.commit()
    return {"message": "User added to segment"}


@router.delete("/unassign/")
def unassign_user_from_segment(data: UserSegmentCreate, db: Session = Depends(get_db)):
    relation = db.query(UserSegment).filter_by(
        user_id=data.user_id,
        segment_id=data.segment_id
    ).first()
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    db.delete(relation)
    db.commit()
    return {"message": "User removed from segment"}
