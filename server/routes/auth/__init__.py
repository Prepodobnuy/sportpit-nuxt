from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import create_access_token
from db.session import get_session
from models.user.admin import Admin
from schemas.auth import Credentials


router = APIRouter()


@router.post("/login")
async def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    exec = await session.execute(select(Admin).where(Admin.username == form_data.username))
    user = exec.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=400, detail="incorrect username")
    if not user.password == form_data.password:
        raise HTTPException(status_code=400, detail="incorrect password")

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
