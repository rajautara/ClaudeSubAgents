#!/usr/bin/env python3
"""
rebuild_index.py — Bina semula README.md index domain DARI fail MD dalam
folder extracted/. Index = derived, bukan sumber kebenaran. Run selepas
tambah/padam/kemaskini mana-mana MD → index sentiasa selari, tiada drift.

Guna:
    python .claude/scripts/rebuild_index.py knowledge-base/customer-reports

Setiap MD perlu front-matter YAML di atas, contoh:
---
customer: Acme Corp
file: acme-corp-2026-q1.md
period: 2026 Q1
summary: Report Q1, baki tertunggak RM3,100.
keywords: invois, tunggakan, INV-1078
source: acme-corp-2026-q1.pdf
extracted: 2026-06-24
---
"""
import sys
import re
from pathlib import Path
from datetime import date


def parse_front_matter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def main():
    if len(sys.argv) < 2:
        print("Guna: python .claude/scripts/rebuild_index.py <folder-domain>", file=sys.stderr)
        sys.exit(1)

    domain = Path(sys.argv[1])
    extracted = domain / "extracted"
    if not extracted.exists():
        print(f"[ralat] Tiada folder: {extracted}", file=sys.stderr)
        sys.exit(1)

    rows = []
    orphans = []  # MD tanpa front-matter
    for md in sorted(extracted.glob("*.md")):
        meta = parse_front_matter(md.read_text(encoding="utf-8"))
        if not meta:
            orphans.append(md.name)
            continue
        rows.append({
            "customer": meta.get("customer", "?"),
            "file": f"extracted/{md.name}",
            "period": meta.get("period", "?"),
            "summary": meta.get("summary", ""),
            "keywords": meta.get("keywords", ""),
        })

    domain_title = domain.name.replace("-", " ").title()
    lines = [
        f"# {domain_title} — Index",
        "",
        "> ⚙️ Fail ini AUTO-GENERATE oleh `.claude/scripts/rebuild_index.py`.",
        "> JANGAN edit manual. Run semula script selepas tambah/padam MD.",
        f"> Dikemaskini: {date.today().isoformat()}",
        "",
        "## Struktur",
        "```",
        f"{domain.name}/",
        "├── README.md          ← index (auto-generate)",
        "├── _raw/              ← dokumen asal — JANGAN padam",
        "└── extracted/         ← MD bersih (sumber kebenaran index)",
        "```",
        "",
        "## Senarai report",
        "",
        "| Customer | Fail | Period | Ringkasan | Kata kunci |",
        "|----------|------|--------|-----------|-----------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['customer']} | `{r['file']}` | {r['period']} | {r['summary']} | {r['keywords']} |"
        )
    if not rows:
        lines.append("| _(tiada report lagi)_ | | | | |")

    if orphans:
        lines += ["", "## ⚠️ MD tanpa front-matter (perlu betulkan)"]
        for o in orphans:
            lines.append(f"- `extracted/{o}` — tiada metadata, tak masuk index")

    (domain / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[ok] Index dikemaskini: {domain/'README.md'} ({len(rows)} report"
          + (f", {len(orphans)} orphan" if orphans else "") + ")")


if __name__ == "__main__":
    main()
