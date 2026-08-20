#!/usr/bin/env python3
"""Render the institutional whitepaper to a deterministic, cross-platform PDF."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import html
import pathlib
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from tools.whitepaper import TITLE

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.md"
OUTPUT = ROOT / "docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.pdf"
SECTION = re.compile(r"^## (\d+)\. (.+)$")


def _inline(value: str) -> str:
    escaped = html.escape(value)
    escaped = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    return escaped


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("CBSRTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=22, leading=27, alignment=TA_CENTER, textColor=colors.HexColor("#17324D"), spaceAfter=16),
        "subtitle": ParagraphStyle("CBSRSubtitle", parent=base["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#46586A"), spaceAfter=9),
        "h1": ParagraphStyle("CBSRH1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.HexColor("#17324D"), spaceBefore=12, spaceAfter=8, keepWithNext=True),
        "h2": ParagraphStyle("CBSRH2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=colors.HexColor("#2C5D7C"), spaceBefore=8, spaceAfter=5, keepWithNext=True),
        "body": ParagraphStyle("CBSRBody", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13.2, textColor=colors.HexColor("#1F2933"), spaceAfter=6),
        "bullet": ParagraphStyle("CBSRBullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, leftIndent=14, firstLineIndent=-8, bulletIndent=4, spaceAfter=3),
        "code": ParagraphStyle("CBSRCode", parent=base["Code"], fontName="Courier", fontSize=7.7, leading=10, backColor=colors.HexColor("#F3F5F7"), borderPadding=5, spaceAfter=5),
        "toc": ParagraphStyle("CBSRTOC", parent=base["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13, leftIndent=8, spaceAfter=2),
        "table": ParagraphStyle("CBSRTable", parent=base["BodyText"], fontName="Courier", fontSize=6.6, leading=8.5, textColor=colors.HexColor("#263442"), spaceAfter=2),
    }


def _footer(canvas, document) -> None:
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(colors.HexColor("#CBD5DF"))
    canvas.line(18 * mm, 15 * mm, width - 18 * mm, 15 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#5C6B78"))
    canvas.drawString(18 * mm, 10 * mm, "CBSR v0.11.0 · research decision support · not legal advice")
    canvas.drawRightString(width - 18 * mm, 10 * mm, f"Page {document.page}")
    canvas.restoreState()


def main() -> int:
    markdown = SOURCE.read_text(encoding="utf-8")
    styles = _styles()
    sections = [match.groups() for match in map(SECTION.match, markdown.splitlines()) if match]
    if len(sections) != 28:
        raise SystemExit(f"expected 28 whitepaper sections, found {len(sections)}")
    story = [
        Spacer(1, 34 * mm), Paragraph(_inline(TITLE), styles["title"]), Spacer(1, 6 * mm),
        Paragraph("Institutional technical whitepaper · version 0.11.0 · 20 August 2026", styles["subtitle"]),
        Paragraph("Research release candidate · external peer review and independent legal review not completed", styles["subtitle"]),
        Spacer(1, 8 * mm),
        Paragraph("CBSR provides deterministic research decision support. It is not legal advice, transaction approval or execution authority.", styles["subtitle"]),
        PageBreak(), Paragraph("Contents", styles["h1"]),
    ]
    for number, title in sections:
        story.append(Paragraph(f"{number}. {_inline(title)}", styles["toc"]))
    story.append(PageBreak())

    in_code = False
    for raw in markdown.splitlines()[1:]:
        line = raw.strip()
        if line == "```text" or (line == "```" and not in_code):
            in_code = True
            continue
        if line == "```" and in_code:
            in_code = False
            continue
        if not line or line == "---":
            if line == "---":
                story.append(Spacer(1, 3 * mm))
            continue
        if line.startswith("## "):
            section_match = SECTION.match(line)
            if section_match and int(section_match.group(1)) > 1 and (
                int(section_match.group(1)) % 2 == 1 or int(section_match.group(1)) == 28
            ):
                story.append(PageBreak())
            story.append(Paragraph(_inline(line[3:]), styles["h1"]))
        elif line.startswith("### "):
            story.append(Paragraph(_inline(line[4:]), styles["h2"]))
        elif line.startswith("- "):
            story.append(Paragraph("• " + _inline(line[2:]), styles["bullet"]))
        elif line.startswith("|"):
            if set(line.replace("|", "").replace("-", "").replace(":", "").strip()):
                story.append(Paragraph(_inline(line), styles["table"]))
        elif in_code:
            story.append(Paragraph(_inline(line), styles["code"]))
        else:
            story.append(Paragraph(_inline(line), styles["body"]))

    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=17 * mm, bottomMargin=20 * mm, title=TITLE, author="CBSR project",
        subject="Versioned, citable and time-aware rules for autonomous finance",
        creator="CBSR deterministic ReportLab renderer", invariant=1, pageCompression=1,
    )
    document.build(story, onFirstPage=_footer, onLaterPages=_footer)
    print(f"whitepaper PDF generated: {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
