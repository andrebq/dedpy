.PHONY: build run dist-windows add-dep add-dev-dep install-deps pydoc

DOC_PORT?=8081

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
	go get -u -v github.com/fhmq/hmq && go install github.com/fhmq/hmq

pydoc:
	poetry run python -m pydoc -p $(DOC_PORT)
