from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        init=False,
    )
    name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    adress: Mapped[str]
    pending: Mapped[bool] = mapped_column(default=True, init=False)
    completed: Mapped[bool] = mapped_column(default=False, init=False)
    created_at: Mapped[datetime]


class OrderProduct(Base):
    __tablename__ = "order_product"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        init=False,
    )
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    count: Mapped[int]
