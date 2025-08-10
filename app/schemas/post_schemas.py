# from pydantic import BaseModel, Field
from pydantic import BaseModel, Field, ConfigDict

class PostBase(BaseModel):
    text: str = Field(..., max_length=64)

class PostCreate(PostBase):
    pass

class PostInDB(PostBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)