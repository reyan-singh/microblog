from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class User(Base):
    """
    Defines the User model for the database.
    This corresponds to the 'users' table.
    """
    __tablename__ = "users"

    # The primary key for the table
    id = Column(Integer, primary_key=True, index=True)

    # The user's unique username
    username = Column(String(50), unique=True, index=True, nullable=False)

    # The user's securely hashed password
    hashed_password = Column(String(255), nullable=False)