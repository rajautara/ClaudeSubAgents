---
name: kb-lookup
description: >
  Use when answering questions from the internal knowledge-base/ folder.
  Provides the lookup procedure, source-citation rules, and the index-first
  reading pattern that keeps context usage low. Triggers on questions about
  SOP, product specs, pricing, organizational info, or any "apa SOP untuk...",
  "berapa harga...", "macam mana proses..." style query about internal docs.
---

# Knowledge-Base Lookup

Panduan untuk mencari dan menjawab dari `knowledge-base/`.

## Prinsip teras

1. **Index-first.** Sentiasa baca `README.md` (master atau domain) sebelum baca
   fail individu. Index memberi peta — elak baca buta semua fail.
2. **Read-only.** Tiada operasi tulis. Hanya Read, Grep, Glob.
3. **Source-grounded.** Setiap fakta mesti boleh dijejak ke fail tertentu.
   Nyatakan path fail sumber.
4. **No hallucination.** Tiada dalam KB = kata "tiada dalam knowledge base".

## Prosedur lookup

```
Soalan masuk
   │
   ├─ Domain jelas? ──ya──► Baca knowledge-base/<domain>/README.md
   │      │
   │      tidak
   │      ▼
   │   Baca knowledge-base/README.md (master index)
   │      │
   ▼      ▼
Grep istilah kunci merentas domain (cth: grep -ri "ar-rahnu" knowledge-base/)
   │
   ▼
Read fail paling relevan SAHAJA (1–3 fail)
   │
   ▼
Susun jawapan + nyatakan path sumber
```

## Format jawapan

- Jawapan ringkas dan tepat.
- Petik nombor/harga/langkah persis seperti tertulis.
- Hujung jawapan: `Sumber: <domain>/<path>.md`
- Kalau >1 sumber: senaraikan semua.
- Kalau bercanggah: tunjuk kedua-dua versi + flag percanggahan.

## Maintenance KB (untuk pengguna, bukan agent)

Agar lookup tepat:
- Setiap domain WAJIB ada `README.md` sebagai index.
- Satu topik = satu fail (`ar-rahnu-workflow.md`, bukan campur dalam `misc.md`).
- Guna heading jelas dalam setiap fail supaya grep mudah jumpa.
- Letak kata kunci/istilah biasa dalam README index untuk bantu carian.
