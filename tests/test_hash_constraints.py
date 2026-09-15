# Copyright the Cross-Border Stablecoin Register contributors.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pathlib
import json
import shutil
import urllib.error

import pytest
from packaging.requirements import Requirement
from packaging.tags import Tag

from tools.hash_constraints import (
    LockError,
    Pin,
    TARGETS,
    Wheel,
    _metadata_wheels,
    _fetch_pypi,
    _bootstrap_closure,
    _read_pins,
    build_outputs,
    load_pin_sets,
    offline_fetcher,
    render_lock,
    validate_dependency_closure,
    validate_project_roots,
    wheel_supports,
)


LINUX_310 = next(target for target in TARGETS if target.key == "linux-cp310-x86_64")
LINUX_313 = next(target for target in TARGETS if target.key == "linux-cp313-x86_64")
WINDOWS_312 = next(target for target in TARGETS if target.key == "windows-cp312-amd64")


def pin(text: str, line: int = 1) -> Pin:
    return Pin(Requirement(text), "fixture.txt", line)


def wheel(tag: Tag, requires_python: str | None = ">=3.10") -> Wheel:
    return Wheel(
        filename="demo-1.0-py3-none-any.whl",
        sha256="a" * 64,
        url="https://files.pythonhosted.org/packages/demo.whl",
        requires_python=requires_python,
        tags=frozenset({tag}),
    )


def test_wheel_compatibility_covers_pure_exact_and_abi3_tags() -> None:
    pure = wheel(Tag("py3", "none", "any"))
    linux_exact = wheel(Tag("cp310", "cp310", "manylinux_2_17_x86_64"))
    windows_exact = wheel(Tag("cp312", "cp312", "win_amd64"))
    linux_abi3 = wheel(Tag("cp39", "abi3", "manylinux2014_x86_64"))

    assert all(wheel_supports(pure, target) for target in TARGETS)
    assert wheel_supports(linux_exact, LINUX_310)
    assert not wheel_supports(linux_exact, WINDOWS_312)
    assert wheel_supports(windows_exact, WINDOWS_312)
    assert not wheel_supports(windows_exact, LINUX_313)
    assert wheel_supports(linux_abi3, LINUX_313)


def test_python_and_platform_markers_are_evaluated_per_target() -> None:
    old_python = pin('exceptiongroup==1.3.1; python_version < "3.11"')
    windows = pin('colorama==0.4.6; sys_platform == "win32"')

    assert old_python.active(LINUX_310)
    assert not old_python.active(LINUX_313)
    assert windows.active(WINDOWS_312)
    assert not windows.active(LINUX_310)


def test_dependency_closure_rejects_a_missing_windows_conditional() -> None:
    app = pin("demo==1.0")
    metadata = {
        ("demo", "1.0"): {
            "requires_dist": ['colorama>=0.4.6; sys_platform == "win32"'],
        },
    }
    with pytest.raises(LockError, match="windows-cp312-amd64.*colorama"):
        validate_dependency_closure([app], metadata)

    colorama = pin('colorama==0.4.6; sys_platform == "win32"', 2)
    metadata[("colorama", "0.4.6")] = {"requires_dist": []}
    validate_dependency_closure([app, colorama], metadata)


def test_official_metadata_excludes_sdist_and_rejects_nonofficial_urls() -> None:
    payload = {
        "info": {"name": "demo", "version": "1.0", "requires_dist": []},
        "urls": [
            {
                "packagetype": "sdist",
                "filename": "demo-1.0.tar.gz",
                "url": "https://files.pythonhosted.org/packages/demo.tar.gz",
                "digests": {"sha256": "b" * 64},
                "yanked": False,
            },
            {
                "packagetype": "bdist_wheel",
                "filename": "demo-1.0-py3-none-any.whl",
                "url": "https://files.pythonhosted.org/packages/demo.whl",
                "digests": {"sha256": "a" * 64},
                "requires_python": ">=3.10",
                "yanked": False,
            },
        ],
    }
    _info, wheels = _metadata_wheels("demo", "1.0", payload)
    assert [item.filename for item in wheels] == ["demo-1.0-py3-none-any.whl"]

    payload["urls"][1]["url"] = "https://example.test/demo.whl"
    with pytest.raises(LockError, match="non-official wheel URL"):
        _metadata_wheels("demo", "1.0", payload)


def test_rendered_lock_enforces_hashes_and_binary_only() -> None:
    requirement = pin("demo==1.0")
    selected = {("demo", "1.0", ""): [wheel(Tag("py3", "none", "any"))]}
    rendered = render_lock("runtime lock", [requirement], selected)

    assert "--require-hashes" in rendered
    assert "--only-binary=:all:" in rendered
    assert "--hash=sha256:" + "a" * 64 in rendered
    assert "+    --hash" not in rendered


def test_committed_pin_sources_cover_windows_runtime_conditionals() -> None:
    root = pathlib.Path(__file__).resolve().parents[1]
    runtime = load_pin_sets(root)["runtime"]
    active_windows = {item.name: item.version for item in runtime if item.active(WINDOWS_312)}
    active_linux = {item.name for item in runtime if item.active(LINUX_313)}

    assert active_windows["colorama"] == "0.4.6"
    assert active_windows["pywin32"] == "312"
    assert "colorama" not in active_linux
    assert "pywin32" not in active_linux


@pytest.mark.parametrize("tag", [
    Tag("cp313", "cp313t", "manylinux_2_17_x86_64"),
    Tag("cp313", "cp313d", "manylinux_2_17_x86_64"),
    Tag("py3", "cp313t", "any"),
    Tag("cp313", "cp313", "manylinux_2_40_x86_64"),
    Tag("cp313", "cp313", "manylinux_3_0_x86_64"),
    Tag("cp313", "cp313", "linux_x86_64"),
    Tag("cp313", "cp313", "musllinux_1_2_x86_64"),
])
def test_standard_ubuntu_target_excludes_incompatible_abi_and_platform(tag: Tag) -> None:
    assert not wheel_supports(wheel(tag), LINUX_313)


def test_generic_older_python_tag_works_on_newer_interpreter() -> None:
    assert wheel_supports(wheel(Tag("py310", "none", "any")), LINUX_313)
    assert not wheel_supports(wheel(Tag("py313", "none", "any")), LINUX_310)


def test_project_and_pin_extras_propagate_transitively() -> None:
    app = pin("demo==1.0")
    dependency = pin("optional==1.0", 2)
    metadata = {
        ("demo", "1.0"): {"requires_dist": ['optional[child]>=1; extra == "feature"']},
        ("optional", "1.0"): {"requires_dist": ['leaf>=1; extra == "child"']},
        ("leaf", "1.0"): {"requires_dist": []},
    }
    roots = [Requirement("demo[feature]>=1")]
    with pytest.raises(LockError, match="optional.*leaf"):
        validate_dependency_closure([app, dependency], metadata, roots=roots)
    validate_dependency_closure([app, dependency, pin("leaf==1.0", 3)], metadata, roots=roots)
    with pytest.raises(LockError, match="optional.*leaf"):
        validate_dependency_closure([pin("demo[feature]==1.0"), dependency], metadata)


def test_direct_url_dependencies_are_rejected_at_all_boundaries(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "fixture.txt"
    path.write_text("demo @ https://example.test/demo.whl\n", encoding="utf-8")
    with pytest.raises(LockError, match="direct URL"):
        _read_pins(path)
    project = tmp_path / "pyproject.toml"
    project.write_text('[project]\ndependencies = ["demo @ https://example.test/demo.whl"]\n', encoding="utf-8")
    with pytest.raises(LockError, match="direct URL"):
        validate_project_roots(tmp_path, [pin("demo==1.0")], include_dev=False)
    metadata = {("demo", "1.0"): {"requires_dist": [
        'demo @ https://example.test/demo.whl ; sys_platform == "not-this-platform"'
    ]}}
    with pytest.raises(LockError, match="direct URL"):
        validate_dependency_closure([pin("demo==1.0")], metadata)


def test_bootstrap_dependency_extras_are_not_lost() -> None:
    pins = [pin(f"{name}==1.0") for name in ("pip", "setuptools", "wheel", "optional", "leaf")]
    metadata = {(item.name, item.version): {"requires_dist": []} for item in pins}
    metadata[("wheel", "1.0")]["requires_dist"] = ["optional[child]>=1"]
    metadata[("optional", "1.0")]["requires_dist"] = ['leaf>=1; extra == "child"']
    assert _bootstrap_closure(pins, metadata) == {item.name for item in pins}


def test_offline_check_rebuilds_every_committed_output_without_network(monkeypatch: pytest.MonkeyPatch) -> None:
    root = pathlib.Path(__file__).resolve().parents[1]
    monkeypatch.setattr("urllib.request.urlopen", lambda *args, **kwargs: pytest.fail("offline check requested network"))
    outputs = build_outputs(root, fetcher=offline_fetcher(root))
    assert len(outputs) == 5
    for path, rendered in outputs.items():
        assert path.read_text(encoding="utf-8") == rendered, path.name


def test_offline_check_rejects_source_drift(tmp_path: pathlib.Path) -> None:
    root = pathlib.Path(__file__).resolve().parents[1]
    shutil.copytree(root / "constraints", tmp_path / "constraints")
    shutil.copyfile(root / "pyproject.toml", tmp_path / "pyproject.toml")
    path = tmp_path / "constraints/runtime.txt"
    path.write_text(path.read_text(encoding="utf-8") + "\n# source edit\n", encoding="utf-8")
    with pytest.raises(LockError, match="source drift"):
        offline_fetcher(tmp_path)


def test_offline_check_rejects_forged_metadata_endpoint(tmp_path: pathlib.Path) -> None:
    root = pathlib.Path(__file__).resolve().parents[1]
    shutil.copytree(root / "constraints", tmp_path / "constraints")
    shutil.copyfile(root / "pyproject.toml", tmp_path / "pyproject.toml")
    path = tmp_path / "constraints/hash-provenance.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    release_key = next(iter(data["releases"]))
    data["releases"][release_key]["metadata"] = "https://example.test/fake"
    path.write_text(json.dumps(data), encoding="utf-8")
    replay = offline_fetcher(tmp_path)
    with pytest.raises(LockError, match="non-official metadata endpoint"):
        replay(*release_key.split("=="))


def test_metadata_transient_error_retries_are_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = []
    waits = []
    def unavailable(*args, **kwargs):
        attempts.append(1)
        raise urllib.error.URLError("transient TLS EOF")
    monkeypatch.setattr("urllib.request.urlopen", unavailable)
    monkeypatch.setattr("tools.hash_constraints.time.sleep", waits.append)
    with pytest.raises(urllib.error.URLError, match="transient TLS EOF"):
        _fetch_pypi("demo", "1.0")
    assert len(attempts) == 3
    assert waits == [1, 2]


def test_metadata_missing_release_is_not_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = []
    def missing(*args, **kwargs):
        attempts.append(1)
        raise urllib.error.HTTPError("https://pypi.org", 404, "Not Found", {}, None)
    monkeypatch.setattr("urllib.request.urlopen", missing)
    monkeypatch.setattr("tools.hash_constraints.time.sleep", lambda *args: pytest.fail("404 retry"))
    with pytest.raises(urllib.error.HTTPError):
        _fetch_pypi("demo", "1.0")
    assert len(attempts) == 1
