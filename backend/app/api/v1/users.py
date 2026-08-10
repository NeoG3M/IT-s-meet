from fastapi import APIRouter, Depends, Response, HTTPException

from app.schemas import UserShort, CreateUser, UserFull
from app.repository.auth import CurrentUser
from app.repository.users import get_short_users
from app.service import user_creation, giving_one_user
from app.database import SessionDep

router = APIRouter()

@router.get('/users', response_model=list[UserShort])
async def get_all_users(current_user: CurrentUser, session: SessionDep, faculty: int | None = None, course: int | None = None):
    users: list[UserShort] = await get_short_users(current_user=current_user, faculty=faculty, course=course, session=session)
    return users

@router.post('/users', status_code=201)
async def create_user(user_data: CreateUser, session: SessionDep):
    user = await user_creation(user_data, session)
    if user:
        return {
        "message": "User has been successfully created.",
        "user_id": user.id
    }
    raise HTTPException(status_code=500, detail='Something went wrong while creating user.')

@router.get('/users/{user_id}', response_model=UserFull)
async def get_user_by_id(user_id: int, current_user: CurrentUser, session: SessionDep):
    # This function can raise HTTPError in case if requested user's privacy doesn't allow current user to show information.
    # That means that frontend must handle this by parsing information by itself
    # But... maybe someday i will change that. For example, when i get to that specific part
    user_info = await giving_one_user(user_id=user_id, current_user=current_user, session=session)
    return user_info


# TODO: patch for: /users/{id}; /users/{id}/skills; /users/{id}/interests
# @router.patch()