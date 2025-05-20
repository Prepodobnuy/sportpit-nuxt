import asyncio

from fastapi import Depends
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
        user = Admin(username="admin", password="admin")
        session.add(user)
        await session.commit()


if __name__ == "__main__":
    main()
    # asyncio.run(create_admin())
