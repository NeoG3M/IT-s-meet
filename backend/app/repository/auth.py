from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.models import User
from app.database import SessionDep

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/api/auth/login"
# )

# TODO: later add token: str = Depends(oauth2_scheme) to func args



async def get_current_user(user_id: int, session: SessionDep) -> User:
    # TODO: JWT descript or TG connection
    query = select(User).where(User.id==user_id)
    result = await session.execute(query)
    user = result.scalars().one()
    if not User:
        raise HTTPException(status_code=404, detail="User with UID {user_id} was not found!")

    return user


CurrentUser = Annotated[
    User,
    Depends(get_current_user)
]