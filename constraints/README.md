# Dependency constraints

`runtime.txt` locks the complete clean-wheel runtime graph and `dev.txt` locks
every additional verification/build dependency. `pyproject.toml` remains the
source of direct supported ranges. The supported interpreter interval is bounded
to CPython 3.10-3.13 so an untested future interpreter cannot be implied.
The refresh helper ignores prereleases and versions whose published files have
all been yanked.

Install exactly the release-tested graph:

```bash
python -m pip install --constraint constraints/dev.txt pip setuptools wheel
python -m pip install --constraint constraints/dev.txt ".[dev]"
```

Check whether a refresh is available without changing files:

```bash
python tools/refresh_constraints.py --check
```

Create a reviewed proposal locally. First update direct pins inside their reviewed
windows, then resolve in a disposable Python 3.10 environment and replace every
transitive pin with the exact `pip freeze --all` result (excluding the local
`cbsr-mcp` path line). Repeat the resolution check on 3.11-3.13 before review:

```bash
python tools/refresh_constraints.py --write
python -m pip install --upgrade --constraint constraints/dev.txt pip setuptools wheel
python -m pip install --upgrade --constraint constraints/dev.txt ".[dev]"
python -m pip freeze --all
python -m tools.verify
```

The refresh helper only selects direct versions inside `pyproject.toml`; it does
not silently rewrite transitives. The human-reviewed freeze is deliberate. Never
merge a refresh until the Linux Python 3.10-3.13 matrix and Windows clean-room job
both pass. Attach the matrix artifact, clean-wheel smoke report and `pip-audit.json`.
