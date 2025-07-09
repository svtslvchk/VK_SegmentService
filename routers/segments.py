from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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



