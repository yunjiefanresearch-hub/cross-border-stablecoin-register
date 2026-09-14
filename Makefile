.PHONY: setup build test verify run

setup:
	python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt
	python -m build --wheel --no-isolation --outdir artifacts/local-wheel
	python tools/install_local_wheel.py --wheel-dir artifacts/local-wheel

build:
	python build.py

test:
	python -m pytest -q

verify:
	python -m tools.verify

run:
	python mcp_server.py
