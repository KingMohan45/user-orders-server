from typing import List

import csv
import typer
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker

from db import non_autocommit_engine
from app.models import Products
from app.schema import ProductSchema
from app.utils import get_uuid

cli = typer.Typer()


def get_products_data() -> List[List]:  
    with open('commands/data/products.csv') as csvFile:
        spamreader = csv.reader(csvFile, delimiter=',', quotechar='|')
        products = list(spamreader)
    return products[1:] # skipping the header


@cli.command()
def seed():
    session = sessionmaker(bind=non_autocommit_engine)()
    try:
        typer.echo("--- Creating products from CSV ---")
        products_data = get_products_data()

        for product_data in products_data:
            typer.echo(f"Creating product: {product_data}")
            code, name, category = product_data
            product_schema = ProductSchema(
                code=code, name=name, category=category
            )
            session.add(Products(id=get_uuid(), **product_schema.dict()))
            session.flush()

        session.commit()
        print("--- Products created successfully. ---")
    except ValidationError as e:
        typer.echo(f"Validation Error: {e}")
        session.rollback()
    except Exception as e:
        typer.echo(f"Error: {e}")
        session.rollback()


if __name__ == "__main__":
    cli()
