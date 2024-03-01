from typing import List, Optional

from fastapi import (
    APIRouter,
    status,
    Depends,
)
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.filters import UserFilter
from app.schema import UserResponseSchema
from app.models import Users
from db import get_autocommit_db

user_router = APIRouter(prefix="", tags=["Users"])


@user_router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(
    params: Params = Depends(),
    session: Session = Depends(get_autocommit_db),
    user_filter: UserFilter = FilterDepends(UserFilter),
) -> Page[UserResponseSchema]:
    """
    This API will verify the provided credentials and return a JWT tokens.
    """
    users = session.query(Users)
    filtered_users = user_filter.filter(users)
    return paginate(filtered_users, params)
