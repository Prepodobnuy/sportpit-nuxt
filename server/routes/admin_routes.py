import json

from itertools import product
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import get_user
from db.session import get_session
from models import cathegory
from models.cathegory.cathegory import Cathegory
from models.cathegory.product import Product
from models.user.admin import Admin
from schemas.order import CathegoryPostScheme, CathegoryScheme, ProductPostScheme, ProductScheme


router = APIRouter()


@router.post("/cathegory")
async def create_cathegory(
    scheme: CathegoryPostScheme,
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        try:
            cathegory = Cathegory(name=scheme.name)
            session.add(cathegory)
            await session.commit()
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.put("/cathegory")
async def update_cathegory(
    scheme: CathegoryScheme,
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        try:
            exec = await session.execute(
                select(Cathegory).where(
                    Cathegory.id == scheme.id,
                )
            )

            cathegory = exec.scalar_one_or_none()

            if cathegory is None:
                raise HTTPException(404)

            cathegory.name = scheme.name

            await session.commit()
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.delete("/cathegory/{cathegory_id}")
async def delete_cathegory(
    cathegory_id: int,
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        try:
            exec = await session.execute(
                select(Cathegory).where(
                    Cathegory.id == cathegory_id,
                )
            )
            cathegory = exec.scalar_one_or_none()

            if cathegory is None:
                raise HTTPException(404)

            product_exec = await session.execute(
                select(Product).where(Product.cathegory_id == cathegory_id)
            )

            products = product_exec.scalars().all()

            for p in products:
                await session.delete(p)

            await session.flush()

            await session.delete(cathegory)

            await session.commit()
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.get("/products")
async def get_products(
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> list[ProductScheme]:
    async with session:
        try:
            exec = await session.execute(select(Product))
            data = exec.scalars().all()

            return [
                ProductScheme(
                    id=d.id,
                    name=d.name,
                    cost=d.cost,
                    count=d.count,
                    cathegory_id=d.cathegory_id,
                )
                for d in data
            ]

        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.post("/product")
async def create_product(
    file: UploadFile = File(...),
    scheme: str = Form(...),
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    if file.content_type is None:
        raise HTTPException(415, "no file supplied")
    if not file.content_type.startswith("image/"):
        raise HTTPException(415, "file is not an image")

    try:
        parsed = ProductPostScheme(**json.loads(scheme))
    except Exception:
        raise HTTPException(400)

    async with session:
        try:
            exec = await session.execute(
                select(Cathegory).where(Cathegory.id == parsed.cathegory_id)
            )

            if exec.scalar_one_or_none() is None:
                raise HTTPException(404)

            content = await file.read()

            product = Product(
                name=parsed.name,
                cost=parsed.cost,
                count=parsed.count,
                cathegory_id=parsed.cathegory_id,
                cover=content,
            )
            session.add(product)
            await session.commit()
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.put("/product/{id}/cover")
async def update_product_cover(
    id: int,
    file: UploadFile = File(...),
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        try:
            exec = await session.execute(select(Product).where(Product.id == id))
            product = exec.scalar_one_or_none()

            if product is None:
                raise HTTPException(404)

            content = await file.read()
            product.cover = content

            await session.commit()

        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.put("/product")
async def update_product(
    scheme: ProductScheme,
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        try:
            exec = await session.execute(select(Product).where(Product.id == scheme.id))
            product = exec.scalar_one_or_none()

            if product is None:
                raise HTTPException(404)

            product.name = scheme.name
            product.cost = scheme.cost
            product.count = scheme.count
            product.cathegory_id = scheme.cathegory_id

            await session.commit()
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.delete("/product/{product_id}")
async def delete_product(
    product_id: int,
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        try:
            exec = await session.execute(select(Product).where(Product.id == product_id))

            product = exec.scalar_one_or_none()

            if product is None:
                raise HTTPException(404)

            await session.delete(product)
            await session.commit()
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.get("/orders/pending")
async def get_pending_orders(
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    pass


@router.get("/orders/completed")
async def get_completed_orders(
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    pass


@router.put("/order/{order_id}/approve")
async def approve_order(
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    pass


@router.delete("/order/{order_id}/decline")
async def decline_order(
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    pass


@router.put("/order/{order_id}/complete")
async def complete_order(
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    pass
