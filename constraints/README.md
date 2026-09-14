# Dependency constraints

`runtime.txt` locks the complete clean-wheel runtime graph and `dev.txt` locks
every additional verification/build dependency. `quality.txt` is the separate
coverage measurement input. These short files are the human-reviewed exact-pin
sources; `pyproject.toml` remains the source of direct supported ranges.

The generated `runtime-hashes.txt`, `dev-hashes.txt`, `quality-hashes.txt`, and
`bootstrap-hashes.txt` add the official SHA-256 for every non-yanked wheel needed
by Ubuntu 24.04 Linux x86_64 (glibc 2.39; excluding wheels requiring newer glibc)
on standard, GIL-enabled CPython 3.10-3.13 and Windows amd64 on CPython 3.12. They also
carry `--require-hashes` and `--only-binary=:all:` as defence in depth. Installation
commands repeat both switches visibly so automated supply-chain checks do not
have to infer security properties hidden in another file. `hash-provenance.json`
records the exact official `pypi.org` metadata endpoint, `files.pythonhosted.org`
URL, filename, `Requires-Python`, and digest behind every allowed wheel. It also
records dependency metadata and normalized source/lock digests for offline checks.

Install exactly the release-tested development graph:

```bash
python -m pip install --require-hashes --only-binary=:all: -r constraints/bootstrap-hashes.txt
python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt
python -m pip check
```

For a clean runtime/package-smoke environment, install the minimal bootstrap lock
first, then `runtime-hashes.txt`. Do not install `dev-hashes.txt` into that environment.
The local wheel must be supplied as its own `file:` requirement with the SHA-256 of
the wheel just built. `tools/package_smoke.py` installs this requirement together
with the runtime hash lock using normal dependency resolution in a clean environment.
The separate `tools/install_local_wheel.py` helper is for development only: after
the complete development graph has been installed, it installs the built local
wheel with `--no-index --no-deps` and then runs `pip check`. It must not be used as
a substitute for the clean runtime dependency-resolution test.

Check whether a refresh is available without changing files:

```bash
python tools/refresh_constraints.py --check
python tools/hash_constraints.py --check-online
```

For repeatable CI and offline verification, `python tools/hash_constraints.py --check`
replays the committed provenance and verifies the complete dependency closure,
source digests, supported-target wheel selection, and all generated lock contents
without a network request. `--check-online` separately checks for current official
metadata drift without writing files. Offline consistency cannot authenticate a
coordinated malicious change to both provenance and locks; source review and the
online refresh comparison remain necessary.

Create a reviewed proposal locally. First update direct pins inside their reviewed
windows, then resolve in disposable target environments and replace every transitive
pin with the exact result (excluding the local `cbsr-mcp` path line). The pin graph
must include marker-only dependencies, not only packages visible on the maintainer's
current platform. In particular, Windows currently activates `colorama` and
`pywin32`; the oldest supported 3.10 patch releases activate an additional
`importlib-metadata`/`zipp` branch. Then regenerate hashes from official PyPI metadata:

```bash
python tools/refresh_constraints.py --write
python tools/hash_constraints.py --write
python tools/hash_constraints.py --check
python -m pip install --require-hashes --only-binary=:all: -r constraints/bootstrap-hashes.txt
python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt
python -m pip check
python -m tools.verify
```

`hash_constraints.py` does not resolve or upgrade versions. It rejects a missing or
conflicting conditional dependency, an unsupported target, a yanked wheel, a source
distribution, a malformed digest, or a download URL outside official PyPI file
hosting. Never hand-edit a generated hash file to make a check pass. The refresh
helper only selects direct versions inside `pyproject.toml`; it does not silently
rewrite transitives. Never merge a refresh until the Linux Python 3.10-3.13 matrix
and Windows clean-room job both pass. Attach the matrix artifact, clean-wheel smoke
report, `pip-audit.json`, and reviewed hash/provenance diff.
