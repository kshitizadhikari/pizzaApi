from pydantic import BaseModel
from typing import Optional


class SignupModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = False

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password123",
                "is_staff": False,
                "is_active": True
            }
        }


class Settings(BaseModel):
    auth_jwt_secret_key: str = 'dd7381b6385a4308695f416342732bf8aee495e8c96f5294b3b38454132094aa'


class LoginModel(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class OrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    order_status: Optional[str] = 'pending'
    pizza_size: Optional[str] = 'small'
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                "quantity": 12,
                "order_status": "pending",
                "pizza_size": "small",
            }
        }