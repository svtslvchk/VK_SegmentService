from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random

from database import get_db
from models import Segment as SegmentModel, UserSegment, User as UserModel
from schemas import Segment, SegmentCreate

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
def get_segments(db: Session = Depends(get_db)):
    return db.query(SegmentModel).all()


@router.delete("/{segment_id}")
def delete_segment(segment_id: int, db: Session = Depends(get_db)):
    segment = db.query(SegmentModel).filter(SegmentModel.id == segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")

    db.delete(segment)
    db.commit()
    return {"message": "Segment and its user relations deleted"}


@router.get("/by-segment/{segment_id}", response_model=List[int])
def get_users_by_segment(segment_id: int, db: Session = Depends(get_db)):
    segment = db.query(SegmentModel).filter(SegmentModel.id == segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")

    return [user.id for user in segment.users]


@router.post("/assign-random")
def assign_random_users(db: Session = Depends(get_db)):
    segments = db.query(SegmentModel).all()
    users = db.query(UserModel).all()

    if not segments or not users:
        raise HTTPException(status_code=400, detail="No segments or users available.")

    assigned_count = 0

    for user in users:
        segment = random.choice(segments)
        existing = db.query(UserSegment).filter_by(user_id=user.id, segment_id=segment.id).first()
        if not existing:
            db.add(UserSegment(user_id=user.id, segment_id=segment.id))
            assigned_count += 1

    db.commit()
    return {"message": f"{assigned_count} users randomly assigned to segments"}
