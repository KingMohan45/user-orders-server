from typing import List

import csv
import typer
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker

from db import non_autocommit_engine
from app.models import Users
from app.schema import UserSchema
from app.utils import get_uuid

cli = typer.Typer()


def get_users_data() -> List[List]:
    users_data = None
    with open('commands/data/users.csv') as csvFile:
        spamreader = csv.reader(csvFile, delimiter=',', quotechar='|')
        users_data = list(spamreader)
    return users_data[1:] # skipping the header


@cli.command()
def seed():
    session = sessionmaker(bind=non_autocommit_engine)()
    try:
        typer.echo("--- Creating users from CSV ---")
        users_data = get_users_data()
        users_obj = []

        for user_data in users_data:
            typer.echo(f"Creating user: {user_data}")
            name, email, phone = user_data
            user_schema = UserSchema(name=name, email=email, phone=phone)
            users_obj.append(Users(id=get_uuid(), **user_schema.dict()))

        session.bulk_save_objects(users_obj)
        session.commit()
        print("--- Users created successfully. ---")
    except ValidationError as e:
        typer.echo(f"Validation Error: {e}")
        session.rollback()
    except Exception as e:
        typer.echo(f"Error: {e}")
        session.rollback()


if __name__ == "__main__":
    cli()
