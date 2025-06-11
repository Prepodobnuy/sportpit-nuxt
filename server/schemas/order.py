from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class ProductScheme(BaseModel):
    id: int
    name: str
    cost: str
    count: int
    cathegory_id: int
    description: str | None


class OrderProductScheme(BaseModel):
    id: int
    count: int
    product: ProductScheme


class OrderProductPostScheme(BaseModel):
    count: int
    product_id: int


class ProductPostScheme(BaseModel):
    name: str
    cost: str
    count: int
    cathegory_id: int
    description: str | None


class CathegoryScheme(BaseModel):
    id: int
    name: str


class CathegoryPostScheme(BaseModel):
    name: str


class OrderScheme(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    adress: str
    pending: bool
    completed: bool
    products: list[OrderProductScheme]
    created_at: datetime


class OrderPostScheme(BaseModel):
    name: str
    phone: str
    email: str
    adress: str
    products: list[OrderProductPostScheme]


class SearchScheme(BaseModel):
    end: bool
    products: list[ProductScheme]


class SearchPostScheme(BaseModel):
    cathegory_id: int
    in_stock_only: bool
    prompt: str
    reversed: bool
    order_by: Literal["name", "cost", "count"]
