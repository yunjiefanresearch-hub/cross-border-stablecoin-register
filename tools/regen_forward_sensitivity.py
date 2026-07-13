# -*- coding: utf-8 -*-
"""
regen_forward_sensitivity.py  (tools/ — SUPERSEDED SHIM)

The original v0.10.1 regeneration lived here and sourced the corrected forward transition set from the
mapper JSX's COMPUTE.corridors. That was a backwards dependency: it made the register non-reproducible
from its own scripts (a canonical rebuild would revert the correction, and CI's `git diff --exit-code`
would fail). As of the v0.10.1 release-consistency pass, the corrected transition set is frozen as a
first-class, version-controlled register input at analysis/forward_transition_set.json, and the
regeneration is a pipeline-native, JSX-free step at scripts/regen_forward_sensitivity.py.

This module is retained only so that any external caller of the old path keeps working; it simply
delegates to the pipeline-native implementation and ignores the legacy JSX argument. Prefer calling
scripts/regen_forward_sensitivity.py directly.
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O passes encoding="utf-8" explicitly throughout.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import runpy
from pathlib import Path

_PIPELINE_IMPL = Path(__file__).resolve().parent.parent / "scripts" / "regen_forward_sensitivity.py"

if __name__ == "__main__":
    if len(_sys.argv) > 1:
        print("note: tools/regen_forward_sensitivity.py is superseded; delegating to "
              "scripts/regen_forward_sensitivity.py (legacy JSX/root arguments are ignored — the "
              "corrected transition set now lives in analysis/forward_transition_set.json).")
    runpy.run_path(str(_PIPELINE_IMPL), run_name="__main__")
