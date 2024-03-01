from datetime import datetime

from sqlalchemy import Column, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_mixin, relationship
from sqlalchemy.types import String, UUID
from db import Base


@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow
    )


@declarative_mixin
class AuditMixin:
    is_active = Column(Boolean, default=True)


class BaseModel(Base, TimestampMixin, AuditMixin):
    __abstract__ = True


class Users(BaseModel):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(36), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20), index=True)


class Products(BaseModel):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, index=True)
    code = Column(String(36), unique=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False, index=True)


class Orders(BaseModel):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    product_id = Column(ForeignKey("products.id"), nullable=False)
    # quantity = Column(String(36), nullable=False)

    # relationships
    user = relationship("Users", backref="orders")
    product = relationship("Products", backref="orders")
