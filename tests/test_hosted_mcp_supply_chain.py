# Copyright the Cross-Border Stablecoin Register contributors.
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import pathlib
import re

import yaml

from tools.verify_security_governance import pinned_action_names


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "hosted-mcp" / "Dockerfile"
WORKFLOW = ROOT / ".github" / "workflows" / "hosted-mcp.yml"
EXPECTED_PYTHON_IMAGE = (
    "python:3.12.14-slim-trixie@"
    "sha256:09f7da3bc104798d0afb40bc08d23ab2da20a76130cec1f2ef170848f5d85217"
)


def dockerfile() -> str:
    return DOCKERFILE.read_text(encoding="utf-8")


def logical_lines(text: str) -> list[str]:
    return [line.strip() for line in re.sub(r"\\\r?\n\s*", " ", text).splitlines()]


def test_hosted_base_image_and_platform_are_immutable() -> None:
    lines = [line for line in logical_lines(dockerfile()) if line.startswith("FROM ")]
    assert lines == [
        f"FROM --platform=linux/amd64 {EXPECTED_PYTHON_IMAGE} AS wheel-builder",
        f"FROM --platform=linux/amd64 {EXPECTED_PYTHON_IMAGE} AS runtime",
    ]


def test_hosted_network_installs_use_canonical_hash_locks() -> None:
    installs = [
        line for line in logical_lines(dockerfile())
        if line.startswith("RUN python -m pip install ")
    ]
    assert len(installs) == 2
    for command in installs:
        assert "--disable-pip-version-check" in command
        assert "--no-cache-dir" in command
        assert "--require-hashes" in command
        assert "--only-binary=:all:" in command
        assert "--requirement /locks/" in command
    assert "dev-hashes.txt" in installs[0]
    assert "runtime-hashes.txt" in installs[1]
    assert "COPY constraints/dev-hashes.txt constraints/runtime-hashes.txt /locks/" in dockerfile()


def test_hosted_local_wheel_install_is_offline_and_hash_checked() -> None:
    text = dockerfile()
    assert "COPY --from=wheel-builder /wheel/ /wheel/" in text
    assert "RUN python /tmp/install_local_wheel.py --wheel-dir /wheel" in text

    installer = (ROOT / "tools" / "install_local_wheel.py").read_text(encoding="utf-8")
    for flag in ["--require-hashes", "--only-binary=:all:", "--no-index", "--no-deps"]:
        assert flag in installer


def test_hosted_runtime_is_non_root_and_does_not_copy_source_tree() -> None:
    runtime = dockerfile().split(" AS runtime", maxsplit=1)[1]
    assert "USER 10001:10001" in runtime
    assert "COPY src/" not in runtime
    assert "COPY ." not in runtime
    assert "CBSR_OBS_LOG=/app/var/obs.jsonl" in runtime


def test_hosted_compatibility_requirements_delegate_to_hash_lock() -> None:
    requirements = (ROOT / "hosted-mcp" / "requirements.txt").read_text(encoding="utf-8")
    active = [line.strip() for line in requirements.splitlines() if line.strip() and not line.startswith("#")]
    assert active == [
        "--require-hashes",
        "--only-binary=:all:",
        "-r ../constraints/runtime-hashes.txt",
    ]


def test_hosted_context_is_default_deny() -> None:
    ignore = (ROOT / "hosted-mcp" / "Dockerfile.dockerignore").read_text(encoding="utf-8")
    active = [
        line.strip() for line in ignore.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert active[0] == "**"
    assert "!constraints/runtime-hashes.txt" in active
    assert "!constraints/dev-hashes.txt" in active
    assert "!tools/install_local_wheel.py" in active
    assert not any(line in {"!.env", "!.git", "!.venv"} for line in active)


def test_hosted_smoke_workflow_is_read_only_and_immutable() -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["jobs"]["container-smoke"]["permissions"] == {"contents": "read"}
    assert pinned_action_names(workflow) == {"actions/checkout"}


def test_hosted_smoke_never_publishes_or_deploys() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "--publish 127.0.0.1::8000" in text
    assert "trap cleanup EXIT" in text
    assert 'docker rm --force "$CONTAINER_NAME"' in text
    assert '"http://127.0.0.1:${port}/health"' in text
    assert '"http://127.0.0.1:${port}/mcp"' in text
    for forbidden in ["docker push", "build-push-action", "kubectl", "fly deploy", "railway", "render deploy"]:
        assert forbidden not in text.lower()


def test_hosted_runbook_does_not_publish_on_all_interfaces() -> None:
    runbook = (ROOT / "hosted-mcp" / "README.md").read_text(encoding="utf-8")
    assert "--publish 127.0.0.1:8000:8000" in runbook
    assert "--publish 8000:8000" not in runbook
    assert "authenticated, TLS-terminating reverse proxy" in runbook
