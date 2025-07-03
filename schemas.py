from typing import List
from pydantic import BaseModel


# --- User schemas ---

class SegmentInUser(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    segments: List[SegmentInUser] = []

    class Config:
        orm_mode = True


# --- Segment schemas ---

class UserInSegment(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SegmentBase(BaseModel):
    name: str


class SegmentCreate(SegmentBase):
    pass


class Segment(SegmentBase):
    id: int
    users: List[UserInSegment] = []

    class Config:
        orm_mode = True


# --- For assigning/unassigning ---

class UserSegmentCreate(BaseModel):
    user_id: int
    segment_id: int
