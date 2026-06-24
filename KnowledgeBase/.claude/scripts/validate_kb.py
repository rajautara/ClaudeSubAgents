#!/usr/bin/env python3
"""
validate_kb.py — Semak keselarasan antara folder extracted/ dan _raw/.
Flag isu tanpa mengubah apa-apa (read-only check).

Guna:
    python .claude/scripts/validate_kb.py knowledge-base/customer-reports

Semakan:
  - MD tanpa front-matter (tak akan masuk index)
  - MD tanpa fail asal dalam _raw/ (yatim — asal hilang/dipadam)
  - Fail _raw/ tanpa MD diekstrak (belum diproses)
Pulangkan exit code 1 jika ada isu (sesuai untuk pre-commit/CI).
"""
import sys
import re
from pathlib import Path


def has_front_matter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    return {k.split(":")[0].strip(): k.split(":", 1)[1].strip()
            for k in m.group(1).splitlines() if ":" in k}


def stem_set(folder: Path, exts):
    if not folder.exists():
        return {}
    return {p.stem: p.name for p in folder.iterdir()
            if p.suffix.lower() in exts}


def main():
    if len(sys.argv) < 2:
        print("Guna: python .claude/scripts/validate_kb.py <folder-domain>", file=sys.stderr)
        sys.exit(1)

    domain = Path(sys.argv[1])
    extracted = domain / "extracted"
    raw = domain / "_raw"
    issues = []

    md_files = list(extracted.glob("*.md")) if extracted.exists() else []
    md_stems = {p.stem for p in md_files}

    for md in md_files:
        meta = has_front_matter(md.read_text(encoding="utf-8"))
        if not meta:
            issues.append(f"[front-matter hilang] extracted/{md.name}")
        elif not meta.get("source"):
            issues.append(f"[medan 'source' tiada] extracted/{md.name}")

    raw_stems = stem_set(raw, {".pdf", ".docx", ".xlsx", ".xlsm", ".png", ".jpg", ".jpeg"})

    # MD yatim: ada MD tapi tiada asal dalam _raw
    for md in md_files:
        meta = has_front_matter(md.read_text(encoding="utf-8"))
        src = meta.get("source", "")
        if src and src not in [v for v in raw_stems.values()] and Path(src).stem not in raw_stems:
            issues.append(f"[asal hilang] extracted/{md.name} → _raw/{src} tidak dijumpai")

    # _raw belum diekstrak
    for stem, name in raw_stems.items():
        if stem not in md_stems:
            issues.append(f"[belum diekstrak] _raw/{name} → tiada extracted/{stem}.md")

    if issues:
        print(f"⚠️  {len(issues)} isu ditemui dalam {domain.name}:")
        for i in issues:
            print("  - " + i)
        print("\nCadangan: run `python .claude/scripts/rebuild_index.py "
              f"{domain}` selepas betulkan.")
        sys.exit(1)
    else:
        print(f"✅ {domain.name}: semua selari, tiada isu.")


if __name__ == "__main__":
    main()
