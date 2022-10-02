import os
from typing import Union
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import _auth_utils as auth_utils
from common.date_utils import get_datetime
from common.firebase_credentials import admin_credentials

firebase_credentials = credentials.Certificate(admin_credentials)
firebase_admin.initialize_app(firebase_credentials)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_users(
        max_results: Union[int, None] = 1000,
        page_token: Union[str, None] = None
    ):
    """
    List up to max_results users.
    """
    page = auth.list_users(max_results=max_results, page_token=page_token)
    response = {
        "users": [],
        "page_token": page.next_page_token
    }
    for user in page.users:
        try:
            is_admin = user.custom_claims["admin"]
        except TypeError:
            is_admin = False
        response["users"].append({
            "uid": user.uid,
            "email": user.email,
            "is_admin": is_admin,
            "active": not user.disabled
        })
    return response    

@app.get("/{uid}")
async def get_user(uid: str):
    """
    Get information about a specific user.
    """
    try:
        user = auth.get_user(uid)
    except auth_utils.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    creation_datetime = get_datetime(user.user_metadata.creation_timestamp)
    last_sign_in_datetime = get_datetime(user.user_metadata.last_sign_in_timestamp)
    try:
        is_admin = user.custom_claims["admin"]
    except TypeError:
        is_admin = False
    return {
        "uid": user.uid,
        "email": user.email,
        "is_admin": is_admin,
        "is_active": not user.disabled,
        "creation_datetime": creation_datetime,
        "last_sign_in_datetime": last_sign_in_datetime
    }

@app.patch("/{uid}")
async def patch_user(uid: str, active: bool):
    """
    Updates the given user's status.
    """
    try:
        auth.update_user(uid, disabled=not active)
    except auth_utils.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
