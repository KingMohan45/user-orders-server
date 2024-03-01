import typer

from commands import users, products, orders
cli = typer.Typer()

cli.add_typer(users.cli, name="users")
cli.add_typer(products.cli, name="products")
cli.add_typer(orders.cli, name="orders")

if __name__ == "__main__":
    cli()
