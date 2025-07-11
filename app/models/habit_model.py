import uuid
from datetime import datetime
from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.routes.habit_route import HabitFrequency

class Habit(Base):
    __tablename__ = "habits"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    frequency = Column(Enum(HabitFrequency, name="habit_frequency"), nullable=False)
    last_done = Column(datetime(), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="habits")