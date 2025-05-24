import json

from itertools import product
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import Select, select
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
    OrderProductScheme,
    OrderScheme,
    ProductPostScheme,
    ProductScheme,
)


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


async def get_orders(query: Select, session: AsyncSession) -> list[OrderScheme]:
    order_product_query = lambda i: select(OrderProduct).where(OrderProduct.order_id == i)
    order_schemas = []

    async with session:
        orders = (await session.execute(query)).scalars().all()

        for order in orders:
            p = (await session.execute(order_product_query(order.id))).scalars().all()
            order_products: list[OrderProductScheme] = []

            for v in p:
                product = (
                    await session.execute(select(Product).where(Product.id == v.product_id))
                ).scalar_one_or_none()
                if product is None:
                    continue
                count = v.count

                order_product = OrderProductScheme(
                    id=v.id,
                    count=count,
                    product=ProductScheme(
                        id=product.id,
                        name=product.name,
                        cost=product.cost,
                        count=product.count,
                        cathegory_id=product.cathegory_id,
                    ),
                )

                order_products.append(order_product)

            order_scheme = OrderScheme(
                id=order.id,
                name=order.name,
                phone=order.phone,
                email=order.email,
                adress=order.adress,
                pending=order.pending,
                completed=order.completed,
                products=order_products,
                created_at=order.created_at,
            )
            order_schemas.append(order_scheme)

    return order_schemas


@router.get("/orders/pending")
async def get_pending_orders(
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> list[OrderScheme]:
    query = select(Order).where(Order.pending == True, Order.completed == False)
    async with session:
        try:
            orders = await get_orders(query, session)
            return orders

        except Exception:
            raise HTTPException(500)


@router.get("/orders/working")
async def get_working_orders(
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> list[OrderScheme]:
    query = select(Order).where(Order.pending == False, Order.completed == False)
    async with session:
        try:
            orders = await get_orders(query, session)
            return orders

        except Exception:
            raise HTTPException(500)


@router.get("/orders/completed")
async def get_completed_orders(
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> list[OrderScheme]:
    query = select(Order).where(Order.pending == False, Order.completed == True)
    async with session:
        try:
            orders = await get_orders(query, session)
            return orders

        except Exception:
            raise HTTPException(500)


@router.put("/order/{order_id}/approve")
async def approve_order(
    order_id: int,
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    query = select(Order).where(Order.id == order_id)
    products_query = select(OrderProduct).where(OrderProduct.order_id == order_id)

    def product_query(id: int):
        return select(Product).where(Product.id == id)

    async with session:
        try:
            order = (await session.execute(query)).scalar_one_or_none()
            if order is None:
                raise HTTPException(404)

            if order.pending:
                order.pending = False
                order_products = (await session.execute(products_query)).scalars().all()
                for op in order_products:
                    product = (
                        await session.execute(product_query(op.product_id))
                    ).scalar_one_or_none()

                    if product is None:
                        continue
                    product.count -= op.count

            else:
                order.completed = True

            await session.commit()

        except Exception:
            await session.rollback()
            raise HTTPException(500)


@router.delete("/order/{order_id}/decline")
async def decline_order(
    order_id: int,
    admin: Admin = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    query = select(Order).where(Order.id == order_id)
    products_query = select(OrderProduct).where(OrderProduct.order_id == order_id)

    def product_query(id: int):
        return select(Product).where(Product.id == id)

    async with session:
        try:
            order = (await session.execute(query)).scalar_one_or_none()
            if order is None:
                raise HTTPException(404)

            if order.pending or order.completed:
                order_products = (await session.execute(products_query)).scalars().all()
                for op in order_products:
                    await session.delete(op)
                await session.flush()
                await session.delete(order)

            elif not order.pending:
                order.pending = True
                order_products = (await session.execute(products_query)).scalars().all()
                for op in order_products:
                    product = (
                        await session.execute(product_query(op.product_id))
                    ).scalar_one_or_none()

                    if product is None:
                        continue
                    product.count += op.count

            await session.commit()

        except Exception as e:
            print(e)
            await session.rollback()
            raise HTTPException(500)
