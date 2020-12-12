.PHONY: build run

build:
	poetry run black .

run:
	poetry run python main.py
