from datetime import datetime, timezone
import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import get_user
from db.session import get_session
from models import cathegory
from models.cathegory.cathegory import Cathegory
from models.cathegory.order import Order, OrderProduct
from models.cathegory.product import Product
from models.user.admin import Admin
from schemas.order import (
    CathegoryPostScheme,
    CathegoryScheme,
    OrderPostScheme,
    ProductPostScheme,
    ProductScheme,
    SearchPostScheme,
    SearchScheme,
)


router = APIRouter()


@router.get("/product/{id}/cover")
async def get_product_cover(
    id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:
    async with session:
        try:
            product = (
                await session.execute(select(Product).where(Product.id == id))
            ).scalar_one_or_none()

            if product is None:
                raise HTTPException(404)

            cover = product.cover

            if cover is None:
                raise HTTPException(404)

            return Response(content=cover, media_type="image/")

        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.get("/cathegories")
async def get_cathegories(session: AsyncSession = Depends(get_session)) -> list[CathegoryScheme]:
    async with session:
        try:
            exec = await session.execute(select(Cathegory))
            cats = exec.scalars().all()

            return [
                CathegoryScheme(
                    id=c.id,
                    name=c.name,
                )
                for c in cats
            ]

        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.post("/order")
async def post_order(
    scheme: OrderPostScheme,
    session: AsyncSession = Depends(get_session),
):
    async with session.begin():
        try:
            order = Order(
                name=scheme.name,
                phone=scheme.phone,
                email=scheme.email,
                adress=scheme.adress,
                created_at=datetime.now(timezone.utc),
            )
            session.add(order)
            await session.flush()

            for p in scheme.products:
                product_order = OrderProduct(
                    order_id=order.id,
                    product_id=p.product.id,
                    count=p.count,
                )
                session.add(product_order)
                await session.flush()

            await session.commit()

        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.post("/search/{index}")
async def search(
    index: int,
    scheme: SearchPostScheme,
    session: AsyncSession = Depends(get_session),
) -> SearchScheme:
    items_per_page = 50
    query = select(Product).where(Product.cathegory_id == scheme.cathegory_id)

    if scheme.prompt != "":
        query = query.where(Product.name.ilike(f"%{scheme.prompt}%"))
    if scheme.in_stock_only:
        query = query.where(Product.count > 0)

    column = Product.name
    count_query = select(func.count()).select_from(query)

    if scheme.order_by == "cost":
        column = Product.cost
    elif scheme.order_by == "count":
        column = Product.count

    if scheme.reversed:
        query = query.order_by(desc(column))
    else:
        query = query.order_by(asc(column))

    query = query.limit(items_per_page).offset(index * items_per_page)

    async with session.begin():
        try:
            total_items = (await session.execute(count_query)).scalar_one()
            total_pages = (total_items + items_per_page - 1) // items_per_page
            result = await session.execute(query)
            products = result.scalars().all()

            if not products:
                return SearchScheme(end=True, products=[])

            return SearchScheme(
                end=index <= total_pages,
                products=[
                    ProductScheme(
                        id=product.id,
                        name=product.name,
                        cost=product.cost,
                        count=product.count,
                        cathegory_id=product.cathegory_id,
                    )
                    for product in products
                ],
            )
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception as e:
            print(e)
            await session.rollback()
            raise HTTPException(500)
