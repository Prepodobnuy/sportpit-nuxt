import asyncio

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session, async_session_maker
from models import create_metadata
from models.user.admin import Admin
from routes import run


def main():
    create_metadata()
    run()


async def create_admin():
    async with async_session_maker() as session:
        users = (
            (await session.execute(select(Admin).where(Admin.username == "admin"))).scalars().all()
        )
        for u in users:
            await session.delete(u)
        await session.flush()
        user = Admin(username="admin", password="adminadmin")
        session.add(user)
        await session.commit()


if __name__ == "__main__":
    main()
    # asyncio.run(create_admin())
