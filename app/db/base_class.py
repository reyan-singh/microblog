# app/db/base_class.py
from sqlalchemy.orm import declarative_base

# This is the base class that all of our SQLAlchemy models will inherit from.
Base = declarative_base()