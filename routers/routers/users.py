from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User as UserModel, UserSegment, Segment as SegmentModel
from schemas import User, UserCreate, UserSegmentCreate

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
    return db_user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/assign/")
def assign_user_to_segment(data: UserSegmentCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == data.user_id).first()
    segment = db.query(SegmentModel).filter(SegmentModel.id == data.segment_id).first()

    if not user or not segment:
        raise HTTPException(status_code=404, detail="User or Segment not found")

    existing = db.query(UserSegment).filter_by(user_id=data.user_id, segment_id=data.segment_id).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already assigned to this segment")

    db.add(UserSegment(user_id=data.user_id, segment_id=data.segment_id))
    db.commit()

    return {"message": f"User {data.user_id} added to segment '{segment.name}'"}


@router.delete("/unassign/")
def unassign_user_from_segment(data: UserSegmentCreate, db: Session = Depends(get_db)):
    relation = db.query(UserSegment).filter_by(user_id=data.user_id, segment_id=data.segment_id).first()

    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")

    db.delete(relation)
    db.commit()

    return {"message": f"User {data.user_id} removed from segment {data.segment_id}"}
