from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    segments: List["Segment"] = []

    class Config:
        orm_mode = True


class SegmentBase(BaseModel):
    name: str


class SegmentCreate(SegmentBase):
    pass


class Segment(SegmentBase):
    id: int
    users: List[int] = []

    class Config:
        orm_mode = True


class UserSegmentCreate(BaseModel):
    user_id: int
    segment_id: int
