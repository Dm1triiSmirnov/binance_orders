install:
	poetry install

lint:
	poetry run flake8 orders

format:
	poetry run black orders
	poetry run isort orders

run:
	python3 manage.py runserver

makemigrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

mm:
	python3 manage.py makemigrations
	python3 manage.py migrate

tests:
	poetry run pytest -vvv

coverage:
	poetry run coverage run -m pytest
	poetry run coverage report -m