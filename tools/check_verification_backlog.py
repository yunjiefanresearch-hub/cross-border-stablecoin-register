#!/usr/bin/env python3
"""check_verification_backlog.py — validate and summarize docs/verification_backlog.json.

The methodology paper (Citable by Construction, §6.2) requires the not-yet-verified residual to be
"published as first-class, queryable data, not concealed behind the headline counts." This makes
that residual machine-checkable: the backlog must parse, carry the required fields, and use only the
declared status values, or the build fails. It prints a summary so a reader (or an agent) can see
the open items and their status at a glance.

Zero third-party dependencies. Exit 0 = valid; exit 1 = a structural problem.
"""
from __future__ import annotations

# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

HERE = pathlib.Path(__file__).resolve().parent
BACKLOG = HERE.parent / "docs" / "verification_backlog.json"

REQUIRED_TOP = {"schema", "version", "generated", "discipline", "status_values", "items"}
REQUIRED_ITEM = {"id", "claim", "jurisdiction", "affects", "status", "open_question", "raised_by"}
J12 = {"US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "JP", "TW", "KR"}


def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    missing_top = REQUIRED_TOP - set(doc)
    if missing_top:
        errs.append(f"top-level keys missing: {sorted(missing_top)}")
        return errs  # can't sensibly continue

    allowed_status = set(doc["status_values"])
    seen_ids = set()

    def check_item(it: dict, where: str, required: set, allow_resolved=False) -> None:
        miss = required - set(it)
        if miss:
            errs.append(f"{where} {it.get('id', '?')}: missing fields {sorted(miss)}")
        iid = it.get("id")
        if iid in seen_ids:
            errs.append(f"{where}: duplicate id {iid!r}")
        seen_ids.add(iid)
        st = it.get("status")
        ok_status = allowed_status | ({"confirmed"} if allow_resolved else set())
        if st not in ok_status:
            errs.append(f"{where} {iid}: status {st!r} not in {sorted(ok_status)}")
        # jurisdiction may be a single code or a slash/space-joined set; check each token
        for tok in str(it.get("jurisdiction", "")).replace("/", " ").split():
            if tok not in J12:
                errs.append(f"{where} {iid}: jurisdiction token {tok!r} not one of the twelve")

    for it in doc["items"]:
        check_item(it, "items", REQUIRED_ITEM)
    for it in doc.get("resolved_since_snapshot", []):
        # resolved items carry a claim/status but 'open_question' is optional
        check_item(it, "resolved_since_snapshot",
                   {"id", "claim", "jurisdiction", "affects", "status", "raised_by"},
                   allow_resolved=True)

    # Light CONTENT check (not just shape): CJK corner brackets must balance. The fourth review
    # caught a broken bracket in VB-04 ("...2026 [ 42..." with two opening brackets) that a
    # shape-only validator waved through; this closes that specific gap.
    raw = json.dumps(doc, ensure_ascii=False)
    n_open = raw.count("\u3014")   # 〔
    n_close = raw.count("\u3015")  # 〕
    if n_open != n_close:
        errs.append(f"unbalanced CJK corner brackets: {n_open} '\u3014' vs {n_close} '\u3015' "
                    f"(a broken bracket like '\u30142026\u3014' instead of '\u30142026\u3015')")
    return errs


def summarize(doc: dict) -> None:
    items = doc["items"]
    from collections import Counter
    by_status = Counter(it["status"] for it in items)
    print("=" * 82)
    print(f"verification backlog  (schema {doc['schema']}, v{doc['version']}, {doc['generated']})")
    print("=" * 82)
    print(f"{len(items)} open/tracked item(s); by status: {dict(by_status)}")
    print("-" * 82)
    for it in items:
        print(f"[{it['status']:>34}]  {it['id']}  ({it['jurisdiction']})  {it['claim']}")
    resolved = doc.get("resolved_since_snapshot", [])
    if resolved:
        print("-" * 82)
        print(f"resolved since the 30 June 2026 snapshot: {len(resolved)}")
        for it in resolved:
            print(f"[{'confirmed':>34}]  {it['id']}  ({it['jurisdiction']})  {it['claim']}")
    print("-" * 82)
    print("Reminder: the gates are defenses, not a cure. Only a primary-source verification pass "
          "retires an item (Citable by Construction \u00a76.1).")
    print("=" * 82)


def main() -> int:
    if not BACKLOG.exists():
        print(f"FATAL: {BACKLOG} not found", file=sys.stderr)
        return 1
    try:
        doc = json.loads(BACKLOG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FATAL: {BACKLOG} is not valid JSON: {exc}", file=sys.stderr)
        return 1
    errs = validate(doc)
    if errs:
        print("[FAIL] verification_backlog.json is malformed:")
        for e in errs:
            print("   -", e)
        return 1
    summarize(doc)
    print("[PASS] verification_backlog.json is well-formed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
