.PHONY: build run dist-windows add-dep add-dev-dep install-deps

build:
	poetry run black .

run:
	poetry run python main.py

dist-windows:
	poetry run pyinstaller main.py

add-dep:
	poetry add $(DEP)

add-dev-dep:
	poetry add -D $(DEP)


install-deps:
	poetry install
