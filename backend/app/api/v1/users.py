from fastapi import APIRouter, Depends, Response, HTTPException

from app.schemas import UserShort, CreateUser
from app.repository.auth import CurrentUser
from app.repository.users import get_short_users
from app.service import user_creation

router = APIRouter()

@router.get('/users', response_model=list[UserShort])
async def get_all_users(current_user: CurrentUser,faculty: int | None = None, course: int | None = None):
    users: list[UserShort] = get_short_users(current_user=current_user, faculty=faculty, course=course)
    return users

@router.post('/users', status_code=201)
async def create_user(user_data: CreateUser):
    user = await user_creation(user_data)
    if user:
        return {
        "message": "User has been successfully created.",
        "user_id": user.id
    }
    raise HTTPException(status_code=500, detail='Something went wrong while creating user.')