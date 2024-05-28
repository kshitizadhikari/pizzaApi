from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from database import Session
from models import Order
from schemas import OrderModel
from utils import get_current_user, get_db

order_router = APIRouter(
    prefix="/orders",
    tags=["Order Routes"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@order_router.get("/")
def index(user: user_dependency):
    return user


@order_router.post("/place-an-order")
def place_order(user: user_dependency, db: db_dependency, order: OrderModel):
    new_order = Order(
        quantity=order.quantity,
        order_status=order.order_status,
        pizza_size=order.pizza_size,
        user_id=user["user_id"]
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
