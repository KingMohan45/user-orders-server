import asyncio

from sqlalchemy.orm import Session

from app.models import Orders
from app.schema import OrderResponseSchema, UserOrdersResponseSchema


async def generate_user_orders(user_id: str, session: Session):
    # Simulate a delay of 10 seconds to generate the file
    await asyncio.sleep(5)

    # Get orders from the database
    orders = session.query(Orders).filter_by(user_id=user_id).all()
    orders_response = [
        OrderResponseSchema(
            id=order.id,
            product_id=order.product_id,
            product_code=order.product.code,
            created_at=order.created_at,
        ) for order in orders
    ]
    return UserOrdersResponseSchema(user_id=user_id, orders=orders_response)