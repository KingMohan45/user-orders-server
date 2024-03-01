from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, StrictStr, EmailStr
from pydantic.v1 import validator

from app.validators import validate_email


class UserSchema(BaseModel):
    name: StrictStr
    email: EmailStr
    phone: StrictStr

    _validate_email = validator("email", allow_reuse=True)(validate_email)


class ProductSchema(BaseModel):
    code: StrictStr
    name: StrictStr
    category: StrictStr


class OrderSchema(BaseModel):
    user_id: StrictStr
    product_id: StrictStr
    created_at: datetime


class UserResponseSchema(UserSchema):
    id: StrictStr

    class Config:
        from_attributes = True


class OrderResponseSchema(BaseModel):
    id: StrictStr
    product_id: StrictStr
    product_code: StrictStr
    created_at: Union[datetime, str]

    def __init__(self, **data):
        super().__init__(**data)
        self.created_at = self.created_at.isoformat()


class UserOrdersResponseSchema(BaseModel):
    user_id: StrictStr
    orders: List[OrderResponseSchema]