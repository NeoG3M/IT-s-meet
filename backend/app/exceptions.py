from fastapi import HTTPException

def raise_user_not_found(uid: int):
    raise HTTPException(status_code=404, detail='User with UID {uid} was not found!')

def raise_rights_exceptions():
    raise ValueError("Fullname argument should be at least 5 characters long.")