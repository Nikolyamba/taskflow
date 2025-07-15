import uuid
from sqlalchemy import Column, String, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_name = Column(String(), unique=True, nullable=False)
    password = Column(String(), unique=False, nullable=False)
    access_token = Column(String(), nullable=False)
    refresh_token = Column(String(), nullable=False)
    telegram_id = Column(BigInteger(), unique=True, nullable=True)

    tasks = relationship("Task", back_populates="user")
    habits = relationship("Habit", back_populates="user")