#!/usr/bin/env python3
"""
ledger_render.py – تبدیل LEDGER.json به LEDGER.md (نسخه انسانی)
"""

import json
from pathlib import Path

def render_ledger():
    root = Path(__file__).parent.parent
    json_path = root / "LEDGER.json"
    md_path = root / "LEDGER.md"

    if not json_path.exists():
        print("LEDGER.json not found. Run this script from repository root.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []
    lines.append("# 📜 The Witness Ledger | شاهدان دفتر")
    lines.append("")
    lines.append("## شاهدان (Witnesses)")
    lines.append("")
    lines.append("| ID | نقش | نام | تاریخ | امضا | تأثیر | RFC | یادداشت |")
    lines.append("|----|------|------|--------|--------|--------|-----|----------|")

    for w in data.get("witnesses", []):
        lines.append(f"| {w.get('id','')} | {w.get('role','')} | {w.get('name','')} | {w.get('date','')} | {w.get('signature','')} | {w.get('impact','')} | {w.get('rfc','')} | {w.get('notes','')} |")

    lines.append("")
    lines.append("## منتقدان (Critics)")
    lines.append("")
    lines.append("| ID | نقش | نام | تاریخ | تأثیر | پذیرفته شد؟ | RFC | یادداشت |")
    lines.append("|----|------|------|--------|--------|-------------|-----|----------|")

    for c in data.get("critics", []):
        lines.append(f"| {c.get('id','')} | {c.get('role','')} | {c.get('name','')} | {c.get('date','')} | {c.get('impact','')} | {c.get('accepted', False)} | {c.get('rfc','')} | {c.get('notes','')} |")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ LEDGER.md updated from {json_path}")

if __name__ == "__main__":
    render_ledger()
