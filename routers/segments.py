from sys import prefix

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import Segment, SegmentCreate
from models import Segment as SegmentModel, UserSegment, User as UserModel
from typing import List
from sqlalchemy.sql.expression import func

router = APIRouter(
    prefix="/segments",
    tags=["Segments"]
)


@router.post("/", response_model=Segment)
def create_segment(segment: SegmentCreate, db: Session = Depends(get_db)):
    db_segment = SegmentModel(name=segment.name)
    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)
    return db_segment


@router.get("/", response_model=List[Segment])
def list_segments(db: Session = Depends(get_db)):
    return db.query(SegmentModel).all()


@router.delete("/{segment_id}")
def delete_segment(segment_id: int, db: Session = Depends(get_db)):
    segment = db.query(SegmentModel).filter(SegmentModel.id == segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    db.delete(segment)
    db.commit()
    return {"message": "Segment deleted"}


@router.get("/by-segment/{segment_id}", response_model=List[int])
def get_users_by_segment(segment_id: int, percentage: float, db: Session = Depends(get_db)):
    relations = db.query(UserSegment).filter(UserSegment.segment_id == segment_id).all()
    return [rel.user_id for rel in relations]


@router.post("/assign-random")
def assign_random_users(segment_id: int, percentage: float, db: Session = Depends(get_db)):
    if not (0 < percentage <= 100):
        raise HTTPException(status_code=400, detail="Percentage must be between 0 and 100")
    total_user = db.query(UserModel).count()
    sample_size = int((percentage / 100) * total_user)
    users = db.query(UserModel).order_by(func.random()).limit(sample_size).all()
    segment = db.query(SegmentModel).filter(SegmentModel.id == segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    for user in users:
        existing = db.query(UserSegment).filter_by(user_id=user.id, segment_id=segment_id).first()
        if not existing:
            db.add(UserSegment(user_id=user.id, segment_id=segment_id))

    db.commit()
    return {"message": f"{sample_size} users assigned to segment '{segment.name}'"}
