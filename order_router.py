from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

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
        name=order.name,
        quantity=order.quantity,
        status=order.status,
        pizza_size=order.pizza_size,
        user_id=user["user_id"]
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@order_router.get("/get-order/{order_id}")
def get_order(db: db_dependency, *, order_id: int, order_name: str):
    db_order = db.query(Order).filter(Order.id == order_id, Order.name == order_name).first()
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid Order Details")
    order_data = {
        "id": db_order.id,
        "name": db_order.name,
        "quantity": db_order.quantity,
        "status": db_order.status.code if db_order.status else None,
        "pizza_size": db_order.pizza_size.code if db_order.pizza_size else None,
        "user_id": db_order.user_id,
    }

    return OrderModel(**order_data)

