from typing import List

import csv
import typer
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker, Session

from db import non_autocommit_engine
from app.models import Orders, Users, Products
from app.schema import OrderSchema
from app.utils import get_uuid

cli = typer.Typer()


def get_orders_data() -> List[List]:  
    with open('commands/data/orders.csv') as csvFile:
        spamreader = csv.reader(csvFile, delimiter=',', quotechar='|')
        orders = list(spamreader)
    return orders[1:] # skipping the header


def fetch_user_id(email: str, session: Session) -> str:
    # find user by email
    user = session.query(Users).filter_by(email=email).first()
    if not user:
        raise ValueError(f"User with email {email} not found.")
    return user.id


def fetch_product_id(code: str, session: Session) -> str:
    # find product by code
    product = session.query(Products).filter_by(code=code).first()
    if not product:
        raise ValueError(f"Product with code {code} not found.")
    return product.id


@cli.command()
def seed():
    session = sessionmaker(bind=non_autocommit_engine)()
    try:
        typer.echo("--- Creating orders from CSV ---")
        orders_data = get_orders_data()

        for order_data in orders_data:
            typer.echo(f"Creating order: {order_data}")
            email, product_code, created_at = order_data
            user_id = fetch_user_id(email, session)
            product_id = fetch_product_id(product_code, session)
            order_schema = OrderSchema(
                user_id=user_id, product_id=product_id, created_at=created_at
            )
            session.add(Orders(id=get_uuid(), **order_schema.dict()))
            session.flush()

        session.commit()
        print("--- Orders created successfully. ---")
    except ValidationError as e:
        typer.echo(f"Validation Error: {e}")
        session.rollback()
    except Exception as e:
        typer.echo(f"Error: {e}")
        session.rollback()


if __name__ == "__main__":
    cli()
