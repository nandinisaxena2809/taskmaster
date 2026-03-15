from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), default="")
    completed = Column(Boolean, default=False)
    priority = Column(String(10), default="medium")
    due_date = Column(DateTime, nullable=True)