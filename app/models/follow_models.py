from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db.base_class import Base

# This is an association table, not a typical model class
followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True)
)