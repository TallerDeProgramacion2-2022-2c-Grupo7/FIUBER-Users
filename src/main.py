from typing import Union
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

all_users = [
    {
        "type": 0,
        "status": 1,
        "id": 1,
        "name": "FIUBER Admin",
        "email": "admin@fi.uber.com",
    },
    {
        "type": 1,
        "status": 1,
        "id": 2,
        "name": "FIUBER User",
        "email": "fiuber.user@gmail.com",
    },
    {
        "type": 1,
        "status": 2,
        "id": 3,
        "name": "FIUBER Blocked User",
        "email": "fiuber.blocked.user@gmail.com",
    }
]

@app.get("/")
async def get_users(
        status: Union[int, None] = None,
        utype: Union[int, None] = None
    ):
    """
    List users matching given query parameters or
    all users if no parameters are specified.
    """
    users = []
    if status is not None:
        users = [user for user in all_users if user["status"] == status]
    else:
        users = all_users
    if utype is not None:
        users = [user for user in users if user["type"] == utype]
    return users

@app.get("/{user_id}")
async def get_user(user_id: int):
    """
    Get information about a specific user.
    """
    try:
        return [user for user in all_users if user["id"] == user_id][0]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

@app.patch("/{user_id}")
async def patch_user(user_id: int, status: int):
    """
    Updates the given user's status.
    """
    for user in all_users:
        if user["id"] == user_id:
            user["status"] = status
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
