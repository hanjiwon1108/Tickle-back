from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.infrastructure.database import Base
from datetime import datetime
import enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    assets = relationship("Asset", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner")
    chat_sessions = relationship("ChatSession", back_populates="owner")
    notifications = relationship("Notification", back_populates="owner")

class AssetType(enum.Enum):
    BANK = "bank"
    STOCK = "stock"
    CRYPTO = "crypto"
    REAL_ESTATE = "real_estate"
    OTHER = "other"

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(AssetType))
    name = Column(String(100))
    balance = Column(Float)
    currency = Column(String(10), default="KRW")
    
    owner = relationship("User", back_populates="assets")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    category = Column(String(50))
    description = Column(String(255))
    date = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="transactions")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session")
    owner = relationship("User", back_populates="chat_sessions")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String(20)) # user, assistant
    content = Column(String(5000)) # Long text
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")

class NotificationType(enum.Enum):
    RECOMMENDATION = "recommendation"  # 상품 추천
    ALERT = "alert"  # 알림/경고
    INFO = "info"  # 정보

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(NotificationType), default=NotificationType.INFO)
    title = Column(String(100))
    message = Column(String(500))
    is_read = Column(Integer, default=0)  # 0: unread, 1: read
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="notifications")
