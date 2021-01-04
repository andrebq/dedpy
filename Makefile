.PHONY: build run dist-windows add-dep add-dev-dep install-deps pydoc busview pyshell runfile

DOC_PORT?=8081

build:
	poetry run black .

run:
	poetry run python main.py editor

FILE?=_scratch.py
runfile:
	poetry run python $(FILE)

busview:
	poetry run python main.py debugger

dist-windows:
	poetry run pyinstaller main.py -n dedpy

pyshell:
	poetry run ipython

add-dep:
	poetry add $(DEP)

add-dev-dep:
	poetry add -D $(DEP)

install-deps:
	poetry install
	go get -u -v github.com/fhmq/hmq && go install github.com/fhmq/hmq

pydoc:
	poetry run python -m pydoc -p $(DOC_PORT)
