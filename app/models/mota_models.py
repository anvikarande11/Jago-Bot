import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    student_uuid = Column(String(36), unique=True, index=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    mobile_number = Column(String(15), nullable=False)
    state = Column(String(100), nullable=False)
    category = Column(String(50), default="ST")  
    annual_family_income = Column(Float, nullable=False)
    digilocker_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to applications
    applications = relationship("ScholarshipApplication", back_populates="student", cascade="all, delete-orphan")


class ScholarshipApplication(Base):
    __tablename__ = "scholarship_applications"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(String(50), unique=True, index=True, nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    scheme_name = Column(String(150), nullable=False)  # e.g., Pre-Matric, Post-Matric, Top Class, etc.
    academic_year = Column(String(20), nullable=False)
    status = Column(String(50), default="Submitted")  # Submitted, Verified, Approved, Disbursed
    disbursed_amount = Column(Float, default=0.0)
    dbt_status = Column(String(50), default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    student = relationship("StudentProfile", back_populates="applications")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(String(36), index=True, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())

    logs = relationship("ChatAuditLog", back_populates="session", cascade="all, delete-orphan")


class ChatAuditLog(Base):
    __tablename__ = "chat_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("chat_sessions.session_id"), nullable=False)
    user_query = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    detected_intent = Column(String(100), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ChatSession", back_populates="logs")