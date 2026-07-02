from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from db.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key = True)
    external_id = Column(String, unique = True, nullable = False)
    marketplace = Column(String, nullable = False)
    product_name = Column(String)
    rating = Column(Integer, nullable = False)
    text = Column(Text)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    status = Column(String, nullable = False, default = "new")

class Response(Base):
    __tablename__ = "responses"
    review_id = Column(Integer, ForeignKey("reviews.id"), primary_key = True)
    sentiment = Column(String, nullable = False)
    suggested_reply = Column(Text)
    needs_human = Column(Boolean, nullable = False)
