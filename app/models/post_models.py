from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(64), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")