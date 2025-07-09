import uuid
from sqlalchemy import Column, String, Enum, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    status = Column(Enum('in_progress', 'done', 'cancelled'))
    due_date = Column(Date())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")