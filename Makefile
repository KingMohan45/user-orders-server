generate-migrations:
	alembic revision --autogenerate -m "$(m)"

migrate:
	alembic upgrade head

start:
	uvicorn main:app --reload

seed-users:
	python cli.py users seed

seed-products:
	python cli.py products seed

seed-orders:
	python cli.py orders seed

seed-all: seed-users seed-products seed-orders

install:
	pip3 install -r requirements.txt
