.PHONY: setup build test verify run

setup:
	python -m pip install --constraint constraints/dev.txt pip setuptools wheel
	python -m pip install --constraint constraints/dev.txt ".[dev]"

build:
	python build.py

test:
	python -m pytest -q

verify:
	python -m tools.verify

run:
	python mcp_server.py
