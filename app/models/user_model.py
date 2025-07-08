import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_name = Column(String(), unique=False, nullable=False)
    access_token = Column(String(), unique=True, nullable=False)
    refresh_token = Column(String(), unique=True, nullable=False)
