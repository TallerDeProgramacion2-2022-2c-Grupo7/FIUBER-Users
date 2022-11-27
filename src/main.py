import os
from typing import Union
from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
import firebase_admin.firestore
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import _auth_utils as auth_utils
from common.date_utils import get_datetime
from common.firebase_credentials import admin_credentials
from middlewares.id_token import IdTokenMiddleware
from datadog import initialize, statsd

options = {
    'statsd_host':'dd-agent',
    'statsd_port':8125
}

initialize(**options)

firebase_credentials = credentials.Certificate(admin_credentials)
firebase_admin.initialize_app(firebase_credentials)
firestore = firebase_admin.firestore.client()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.add_middleware(IdTokenMiddleware)

@app.get("/")
async def get_users(
        max_results: Union[int, None] = 1000,
        page_token: Union[str, None] = None,
    ):
    """
    List up to max_results users.
    """
    statsd.event("An error occurred - FIUBER Users", "Error message", alert_type="error")
    page = auth.list_users(max_results=max_results, page_token=page_token)
    response = {
        "result": [],
        "page_token": page.next_page_token
    }
    for user in page.users:
        try:
            is_admin = user.custom_claims["admin"]
        except TypeError:
            is_admin = False
        response["result"].append({
            "uid": user.uid,
            "email": user.email,
            "is_admin": is_admin,
            "is_active": not user.disabled
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
    try:
        is_admin = user.custom_claims["admin"]
    except TypeError:
        is_admin = False
    user_info = {
        "uid": user.uid,
        "email": user.email,
        "is_admin": is_admin,
        "is_active": not user.disabled,
        "creation_datetime": get_datetime(user.user_metadata.creation_timestamp),
        "last_sign_in_datetime": get_datetime(user.user_metadata.last_sign_in_timestamp)
    }
    profile = firestore.document(f"publicProfiles/{user.uid}").get()
    if profile.exists:
        profile_data = profile.to_dict()
        user_info["first_name"] = profile_data["firstName"]
        user_info["last_name"] = profile_data["lastName"]
    return {"result": user_info}

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
