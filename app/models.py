from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    research_papers = Column(Integer, default=0)
    hackathons_count = Column(Integer, default=0)
    internships_count = Column(Integer, default=0)
    incoscore = Column(Float, default=0.0)
    # Relationship to track applications
    applications = relationship("Application", back_populates="applicant")

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    link = Column(String(500), unique=True)
    university = Column(String(100))
    description = Column(Text)
    domain = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# NEW TABLE FOR PHASE 5
class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    applied_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="Applied") # e.g., Applied, Shortlisted

    applicant = relationship("User", back_populates="applications")