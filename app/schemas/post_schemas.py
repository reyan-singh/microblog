from pydantic import BaseModel, Field

class PostBase(BaseModel):
    text: str = Field(..., max_length=64)

class PostCreate(PostBase):
    pass

class PostInDB(PostBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True