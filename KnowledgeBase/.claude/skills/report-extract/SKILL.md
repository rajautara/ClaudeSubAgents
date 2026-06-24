---
name: report-extract
description: >
  Use when converting source documents (PDF, Word, Excel, scanned images) into
  clean Markdown for the knowledge base — one file per report. Covers the
  extraction toolchain, the standard MD template, naming convention, and index
  updates. Triggers on "extract", "convert PDF to markdown", "process reports",
  "tukar dokumen jadi MD".
---

# Report Extraction → Markdown

Tukar dokumen sumber jadi MD bersih, satu fail per report.

## Toolchain (ikut jenis fail)

| Jenis | Tool | Nota |
|-------|------|------|
| PDF (teks) | pdfplumber | Paling tepat untuk teks + jadual |
| PDF (imbasan) | pytesseract + pdf2image | OCR; perlu tesseract dipasang |
| Word .docx | python-docx | Teks + jadual |
| Excel .xlsx | openpyxl / pandas | Setiap sheet → seksyen |
| Imej | pytesseract | OCR terus |

Install: `pip install pdfplumber python-docx openpyxl pandas --break-system-packages`
OCR (jika perlu): `apt-get install -y tesseract-ocr poppler-utils`

## Template MD standard

```markdown
# <Customer> — <Jenis Report> (<Period>)

> Sumber asal: _raw/<fail-asal>
> Diekstrak: <tarikh>

## Ringkasan
## Maklumat Customer
## Butiran / Transaksi
## Isu / Catatan
## Tindakan Susulan
## Kata Kunci
```

## Naming convention
- `<customer-slug>-<period>.md` — huruf kecil, sengkang, tiada ruang.
- Contoh: `acme-corp-2026-q1.md`, `beta-sdn-bhd-2025-12.md`.

## Peraturan
1. **Satu report = satu fail.** Jangan campur customer.
2. **Heading konsisten** ikut template → grep mudah cari.
3. **Pelihara angka/tarikh persis.** Jangan bundar atau ubah.
4. **Simpan asal** dalam `_raw/` — jangan padam.
5. **Kemaskini index** `README.md` selepas setiap extraction.
6. **Sahkan** dengan baca semula fail MD.
7. Gagal extract → lapor, jangan reka kandungan.

## Aliran

```
_raw/report.pdf
   │  extract_report.py
   ▼
teks mentah
   │  strukturkan ikut template
   ▼
extracted/customer-period.md
   │  kemaskini
   ▼
README.md (index domain)
```
