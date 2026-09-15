#!/usr/bin/env python3
# Copyright the Cross-Border Stablecoin Register contributors.
# SPDX-License-Identifier: Apache-2.0
"""Install this checkout's built wheel without fetching or resolving dependencies.

Install the reviewed, hash-checked dependency graph first. The local wheel is a
build output, so its SHA-256 is calculated immediately before pip verifies it.
This checksum protects the handoff; it is not an independent trust attestation.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys
import tempfile

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def write_wheel_requirement(wheel: pathlib.Path, destination: pathlib.Path) -> str:
    wheel = wheel.resolve(strict=True)
    if not wheel.is_file() or not re.fullmatch(r"cbsr_mcp-[A-Za-z0-9_.+]+-py3-none-any\.whl", wheel.name):
        raise ValueError("expected a CBSR universal wheel built from this checkout")
    digest = hashlib.sha256()
    with wheel.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    value = digest.hexdigest()
    destination.write_text(
        f"cbsr-mcp @ {wheel.as_uri()} --hash=sha256:{value}\n",
        encoding="utf-8", newline="\n",
    )
    return value


def install_command(python: str, requirements: pathlib.Path) -> list[str]:
    return [
        python, "-m", "pip", "install", "--require-hashes", "--only-binary=:all:",
        "--no-index", "--no-deps", "--requirement", str(requirements),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel-dir", type=pathlib.Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()
    wheels = sorted(args.wheel_dir.glob("cbsr_mcp-*.whl"))
    if len(wheels) != 1:
        parser.error("wheel directory must contain exactly one built CBSR wheel")
    with tempfile.TemporaryDirectory(prefix="cbsr-local-install-") as directory:
        manifest = pathlib.Path(directory) / "local-wheel.txt"
        value = write_wheel_requirement(wheels[0], manifest)
        subprocess.run(install_command(args.python, manifest), check=True)
        subprocess.run([args.python, "-m", "pip", "check"], check=True)
    print(f"installed local wheel with SHA-256 verification: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
