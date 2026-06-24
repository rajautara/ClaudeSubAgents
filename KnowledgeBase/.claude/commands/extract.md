---
description: Extract dokumen (PDF/Word/Excel) jadi Markdown — 1 fail per report + kemaskini index
argument-hint: [path fail atau folder] [domain, cth: customer-reports]
---

Extract dokumen menjadi Markdown bersih, SATU fail per report, dengan heading
jelas mengikut template standard. Kemudian kemaskini index domain.

**Input:** $ARGUMENTS

Langkah:
1. Cari fail sumber (Glob/Bash). Simpan asal dalam `_raw/` jika belum ada.
2. Jalankan `python .claude/scripts/extract_report.py <fail>` untuk dapatkan teks.
3. Strukturkan ikut template (Ringkasan, Maklumat Customer, Butiran, Isu,
   Tindakan Susulan, Kata Kunci).
4. Simpan sebagai `extracted/<customer-slug>-<period>.md`.
5. Kemaskini `README.md` index domain (nama, path, period, ringkasan, kata kunci).
6. Baca semula untuk sahkan tiada teks rosak.

Tulis HANYA dalam folder `extracted/`, `_raw/`, dan index README. Jangan reka
kandungan jika extraction gagal — beritahu pengguna.
