import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from app.db import Base


class SocialAccountProviders(enum.Enum):
    FACEBOOK = "facebook.com"
    TWITTER = "twitter.com"
    INSTAGRAM = "instagram.com"
    TIKTOK = "tiktok.com"


class Social(Base):  # type: ignore
    __tablename__ = "socials"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    network = Column(Enum(SocialAccountProviders))
    account_url = Column(String(200), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="social_accounts")
