from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import CreateUser
from app.models import User
from app.repository import create_user

async def user_creation(user_data: CreateUser, session: AsyncSession):
    sign_date = datetime.now()
    new_user = User(tg_id=user_data.tg_id, tg_username=user_data.tg_username, signed_at=sign_date)
    new_user = await create_user(new_user, session)

    return new_user
