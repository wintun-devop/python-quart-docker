from sqlalchemy import (
                        Column, 
                        Integer, 
                        String, 
                        Float, 
                        Text,
                        ForeignKey,
                        func,
                        UniqueConstraint
                        )
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
    id:Mapped[str] = mapped_column(Text,primary_key=True)
    username:Mapped[str] = mapped_column(String,nullable=False,unique=True)
    email:Mapped[str] = mapped_column(String,nullable=False,unique=True)
    password:Mapped[str] = mapped_column(String,nullable=False)
    role:Mapped[str] = mapped_column(String,nullable=True,default="user")
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),onupdate=func.now())
    # 1–1 with UserAttribute
    attribute: Mapped["UserAttribute"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    #1-many with Order
    orders: Mapped[list["Order"]] = relationship(
         back_populates="order",
         cascade="all, delete-orphan",
        passive_deletes=True,
    )

class UserAttribute(Base):
    __tablename__ = "esm_user_attributes"
    id:Mapped[str] = mapped_column(Text,primary_key=True)
    profile_url = mapped_column(Text,nullable=True,default="default.png")
    display_name = mapped_column(Text,nullable=True,default="USER")
    #one_to_one relation with User
    user_id: Mapped[str] = mapped_column(
        Text, ForeignKey("esm_users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),onupdate=func.now())
    

class Inventory(Base):
    __tablename__ = "esm_inventory"
    id:Mapped[str] = mapped_column(Text,primary_key=True)
    name:Mapped[str] = mapped_column(Text,nullable=False)
    model_no:Mapped[str] = mapped_column(String,nullable=False, unique=True)
    price:Mapped[float] = mapped_column(Float,nullable=True,default=0)
    qty:Mapped[int] = mapped_column(Integer,nullable=True,default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),onupdate=func.now())
    # 1–many with OrderedItems (each OrderedItem points to one Inventory)
    ordered_items: Mapped[list["OrderedItems"]] = relationship(
        back_populates="inventory",
        cascade="all, delete-orphan",
    )

class Order(Base):
    __tablename__ = "esm_orders"
    id:Mapped[str] = mapped_column(Text,primary_key=True)
    status:Mapped[str] = mapped_column(String,default="panding")
    user_id:Mapped[str]=mapped_column(
        Text,ForeignKey("esm_users.id",ondelete="RESTRICT"),nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),onupdate=func.now())
    user: Mapped["User"] = relationship(back_populates="orders",)
    # 1–many with OrderedItems
    items: Mapped[list["OrderedItems"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    
class OrderedItems(Base):
    __tablename__ = "esm_ordered_items"
    __table_args__ = (
        UniqueConstraint("order_id", "item_id", name="uq_order_item"),
    )
    id:Mapped[str] = mapped_column(Text,primary_key=True)
    order_qty :Mapped[int] = mapped_column(Integer,nullable=True,default=0)
    order_id: Mapped[str] = mapped_column(
        Text, ForeignKey("esm_orders.id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[str] = mapped_column(
        Text, ForeignKey("esm_inventory.id", ondelete="RESTRICT"), nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),onupdate=func.now())
    order: Mapped["Order"] = relationship(back_populates="items")
    inventory: Mapped["Inventory"] = relationship(back_populates="ordered_items")




