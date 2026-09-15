# Copyright the CBSR contributors.
# SPDX-License-Identifier: Apache-2.0
"""Exercise the pinned measurement tool, not a mocked coverage result."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


def test_coverage_collects_child_and_grandchild_after_changing_directory(tmp_path):
    pytest.importorskip("coverage", reason="measurement integration runs in the Gold tooling job")
    source = tmp_path / "source with spaces"
    source.mkdir()
    child = source / "child.py"
    grandchild = source / "grandchild.py"
    parent = source / "parent.py"
    parent.write_text("import subprocess, sys\nsubprocess.run([sys.executable, 'child.py'], check=True)\n", encoding="utf-8")
    child.write_text("import subprocess, sys\nsubprocess.run([sys.executable, 'grandchild.py'], check=True)\n", encoding="utf-8")
    grandchild.write_text("result = 40 + 2\nassert result == 42\n", encoding="utf-8")
    config = tmp_path / "measure.ini"
    config.write_text("[run]\nbranch = True\npatch = subprocess\nparallel = True\n"
                      f"source = {source.as_posix()}\ndata_file = {(tmp_path / '.coverage').as_posix()}\n", encoding="utf-8")
    environment = {key: value for key, value in os.environ.items() if not key.startswith("COVERAGE_")}
    environment["PYTHONUTF8"] = "1"
    def run(*arguments, cwd=source):
        result = subprocess.run([sys.executable, "-m", "coverage", *arguments], cwd=cwd,
                                env=environment, capture_output=True, text=True, encoding="utf-8", check=False)
        assert result.returncode == 0, result.stdout + result.stderr
    run("run", f"--rcfile={config}", str(parent))
    run("combine", f"--rcfile={config}", cwd=tmp_path)
    output = tmp_path / "coverage.json"
    run("json", f"--rcfile={config}", "-o", str(output), cwd=tmp_path)
    files = json.loads(output.read_text(encoding="utf-8"))["files"]
    by_name = {Path(name).name: data for name, data in files.items()}
    for name in ("parent.py", "child.py", "grandchild.py"):
        assert by_name[name]["summary"]["covered_lines"] == 2
        assert by_name[name]["missing_lines"] == []
