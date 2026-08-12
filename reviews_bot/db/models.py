from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base
from enum import Enum

class ResponseStatus(str, Enum):
    PENDING = "pending"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    SKIPPED = "skipped"

class ReviewStatus(str, Enum):
    NEW = "new"
    PROCESSED = "processed"

class SubscriptionStatus(str, Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    INACTIVE = "inactive"

class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key = True)
    chat_id = Column(String, unique = True, nullable = False)
    brand_name = Column(String, nullable = False)
    subscription_status = Column(String, nullable = False, default = SubscriptionStatus.TRIAL)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    reviews = relationship("Review", back_populates="seller")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key = True)
    external_id = Column(String, unique = True, nullable = False)
    marketplace = Column(String, nullable = False)
    product_name = Column(String)
    rating = Column(Integer, nullable = False)
    text = Column(Text)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    status = Column(String, nullable = False, default = ReviewStatus.NEW)
    priority = Column(Integer, nullable = True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable = True)
    seller = relationship("Seller", back_populates="reviews")

class Response(Base):
    __tablename__ = "responses"
    review_id = Column(Integer, ForeignKey("reviews.id"), primary_key = True)
    sentiment = Column(String, nullable = False)
    suggested_reply = Column(Text)
    needs_human = Column(Boolean, nullable = False)
    status = Column(String, nullable = False, default = ResponseStatus.PENDING)
