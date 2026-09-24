.PHONY: setup setup-deps build test verify run
.DEFAULT_GOAL := setup

# Evaluated after setup-deps, including tomli on Python 3.10. Package version
# comes from pyproject.toml; previous wheels remain in their version directories.
LOCAL_WHEEL_DIR = artifacts/local-wheel/$(shell python -c "from tools.package_release import VERSION; print(VERSION)")

setup-deps:
	python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt

setup: setup-deps
	python -I -X utf8 -m build --wheel --no-isolation --outdir "$(LOCAL_WHEEL_DIR)"
	python tools/install_local_wheel.py --wheel-dir "$(LOCAL_WHEEL_DIR)"

build:
	python build.py

test:
	python -m pytest -q

verify:
	python -m tools.verify

run:
	python mcp_server.py
