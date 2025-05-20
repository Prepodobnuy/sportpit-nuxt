from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        init=False,
    )
    name: Mapped[str]
    cost: Mapped[str]
    count: Mapped[int]
    cathegory_id: Mapped[int] = mapped_column(ForeignKey("cathegory.id"))
    cover: Mapped[bytes | None]
