from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from database import get_db
from models import User, Segment, UserSegment
from schemas import SegmentDistributionRequest

router = APIRouter(
    prefix="/distribute",
    tags=["Distribution"]
)

@router.post("/")
def distribute_segment(data: SegmentDistributionRequest, db: Session = Depends(get_db)):
    segment = db.query(Segment).filter(Segment.id == data.segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")

    all_users = db.query(User).all()
    existing_user_ids = {us.user_id for us in db.query(UserSegment).filter(UserSegment.segment_id == data.segment_id).all()}
    eligible_users = [user for user in all_users if user.id not in existing_user_ids]
    if not eligible_users:
        return {"message": "No eligible users for distribution"}

    n_to_select = int(len(eligible_users) * data.percentage / 100)
    selected_users = random.sample(eligible_users, n_to_select) if n_to_select > 0 else []

    for user in selected_users:
        new_link = UserSegment(user_id=user.id, segment_id=data.segment_id)
        db.add(new_link)

    db.commit()

    return {
        "message": f"Segment distributed to {len(selected_users)} users",
        "segment_id": data.segment_id,
        "assigned_user_ids": [user.id for user in selected_users]
    }
