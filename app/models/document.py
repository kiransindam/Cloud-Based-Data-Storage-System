from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)          # original name
    s3_key = Column(String, unique=True, nullable=False)  # path in S3
    content_type = Column(String, nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    tags = Column(String, default="")                  # comma-separated
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="documents")
