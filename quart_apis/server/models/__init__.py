from sqlalchemy import Column, Integer, String, Float, Text,ForeignKey,func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from typing import List
import datetime,uuid

class Base(AsyncAttrs,DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "esm_users"
    id:Mapped[str] = mapped_column(Text,primary_key=True, default=uuid.uuid4)
    username:Mapped[str] = mapped_column(String,nullable=False,unique=True)
    email:Mapped[str] = mapped_column(String,nullable=False,unique=True)
    password:Mapped[str] = mapped_column(String,nullable=False,unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),onupdate=func.now())


class Inventory(Base):
    __tablename__ = "esm_inventory"
    id:Mapped[str] = mapped_column(Text,primary_key=True, default=uuid.uuid4)
    name:Mapped[str] = mapped_column(Text,nullable=False)
    model_no:Mapped[str] = mapped_column(String,nullable=False, unique=True)
    price:Mapped[float] = mapped_column(Float,nullable=True,default=0)
    qty:Mapped[int] = mapped_column(Integer,nullable=True,default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),onupdate=func.now())
