from fastapi import APIRouter, WebSocket, Depends, status
from pydantic import StrictStr
from sqlalchemy.orm import Session

from app.orders.utils import generate_user_orders
from db import get_autocommit_db
from app.schema import UserOrdersResponseSchema

orders_router = APIRouter(prefix="/orders", tags=["Users"])


@orders_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_users(
    user_id: StrictStr,
    session: Session = Depends(get_autocommit_db),
) -> UserOrdersResponseSchema:
    """
    This API will fetch orders for a user.
    """
    orders: UserOrdersResponseSchema = await generate_user_orders(user_id,session)
    return orders


@orders_router.websocket("/{user_id}/download")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: StrictStr,
    session: Session = Depends(get_autocommit_db),
):
    await websocket.accept()
    await websocket.send_text(f"Fetching orders for user: {user_id}")
    orders: UserOrdersResponseSchema = await generate_user_orders(user_id,session)
    await websocket.send_json(orders.dict())
    await websocket.close()
