#!/usr/bin/env python3
"""v0.7.0 — assign the `claim_class` axis to every record.

The axis is the *epistemic kind* of a record's load-bearing claim, orthogonal to
`evidence_tier` (how well-sourced) and `status` (in force vs draft):

  - tier1_legal       : a proposition of law (what a binding instrument requires/
                        permits/prohibits) — citable to the instrument.
  - tier2_operational : a report of market/operational fact (what is live, who is
                        registered, what launched, rails/liquidity) — as-of-dated.

Mapping rule for the current substrate (audited against every record): the
`implementation_status` dimension is a market/timeline report -> tier2_operational;
all fourteen other dimensions state propositions of law -> tier1_legal. The field is
per-record (not derived at read time) so a future operational claim living inside a
nominally-legal dimension can be tagged tier2_operational explicitly.

This edits the YAML *textually* (insert one line after `confidence:`) to preserve the
maintainer's hand-authored formatting, block scalars, and comments. Idempotent:
re-running makes no change once `claim_class:` is present.

Usage:  python scripts/retag_claim_class_v0_7_0.py
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OPERATIONAL_DIMENSIONS = {"implementation_status"}
TAG = "v0.7.0_claim_class"


def claim_class_for(dimension: str) -> str:
    return "tier2_operational" if dimension in OPERATIONAL_DIMENSIONS else "tier1_legal"


def dimension_of(text: str):
    m = re.search(r"^dimension:\s*(\S+)\s*$", text, re.MULTILINE)
    return m.group(1) if m else None


def add_tag(text: str) -> str:
    """Append the v0.7.0 tag under an existing `tags:` block-list if not present."""
    if TAG in text:
        return text
    # Only handle the block-list style used throughout the register:
    #   tags:
    #   - foo
    #   - bar
    lines = text.splitlines(keepends=True)
    out, i, n = [], 0, len(lines)
    inserted = False
    while i < n:
        line = lines[i]
        out.append(line)
        if not inserted and re.match(r"^tags:\s*$", line):
            j = i + 1
            block = []
            while j < n and re.match(r"^- ", lines[j]):
                block.append(lines[j])
                j += 1
            out.extend(block)
            if block:                      # append our tag at the end of the block
                out.append(f"- {TAG}\n")
                inserted = True
                i = j
                continue
        i += 1
    return "".join(out) if inserted else text


def process(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    if re.search(r"^claim_class:\s*\S+", text, re.MULTILINE):
        return "skip (already tagged)"
    dim = dimension_of(text)
    if dim is None:
        return "skip (no dimension — not an obligation record)"
    cc = claim_class_for(dim)
    # insert `claim_class:` immediately after the first `confidence:` line
    m = re.search(r"^(confidence:.*\n)", text, re.MULTILINE)
    if not m:
        return "ERROR: no confidence line to anchor insertion"
    insert_at = m.end()
    new_text = text[:insert_at] + f"claim_class: {cc}\n" + text[insert_at:]
    new_text = add_tag(new_text)
    path.write_text(new_text, encoding="utf-8")
    return f"{cc}"


def main():
    records = sorted(p for p in ROOT.glob("*.yaml") if p.name != "_TEMPLATE.yaml")
    counts = {"tier1_legal": 0, "tier2_operational": 0, "skipped": 0, "errors": 0}
    for p in records:
        # only touch obligation records (jurisdiction + dimension)
        head = p.read_text(encoding="utf-8")
        if "jurisdiction:" not in head or "dimension:" not in head:
            continue
        result = process(p)
        if result in ("tier1_legal", "tier2_operational"):
            counts[result] += 1
            print(f"  {result:18}  {p.name}")
        elif result.startswith("ERROR"):
            counts["errors"] += 1
            print(f"  !! {result}: {p.name}", file=sys.stderr)
        else:
            counts["skipped"] += 1
    print(f"\nclaim_class assigned — tier1_legal: {counts['tier1_legal']}, "
          f"tier2_operational: {counts['tier2_operational']}, "
          f"skipped: {counts['skipped']}, errors: {counts['errors']}")
    if counts["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
