from models import Order
from schemas import OrderModel

def map_order_to_order_model(order: Order) -> OrderModel:
    return OrderModel(
        id=order.id,
        name=order.name,
        quantity=order.quantity,
        status=order.status.code if order.status else None,
        pizza_size=order.pizza_size.code if order.pizza_size else None,
        user_id=order.user_id
    )
