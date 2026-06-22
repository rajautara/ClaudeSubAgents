# Project Review — Claude Code Setup

Tiga cara cetus review yang sama, dikongsi otak (`project-reviewer` subagent).

## Struktur
```
.claude/
├── agents/
│   └── project-reviewer.md      # OTAK: isolated context, read-only, model: opus
├── commands/
│   └── review-project.md        # Trigger: /review-project [focus]
└── skills/
    └── project-review/
        ├── SKILL.md             # Trigger auto-invocable; delegate ke subagent
        └── reference.md         # Protokol penuh (fallback bila subagent tiada)
```

## Pemasangan
Salin folder `.claude/` ke **root projek** (project scope, boleh commit ke git untuk dikongsi pasukan):
```
cp -r .claude /path/ke/projek-anda/
```
Atau letak di `~/.claude/` (user scope) untuk guna di **semua** projek.
Lepas salin, **restart sesi Claude Code** supaya fail dibaca (agent/skill yang ditambah terus ke disk perlu restart).

## Bila guna yang mana

| Format | Cara cetus | Bila guna |
|---|---|---|
| **Command** `/review-project` | Taip eksplisit | Bila awak nak review sekarang, dengan kawalan penuh. Boleh beri fokus: `/review-project src/api` atau `/review-project security only` |
| **Skill** `project-review` | Auto bila Claude kesan niat ("review my project", "is this well built") | Bila awak nak Claude sendiri tahu bila nak guna, tanpa ingat nama command |
| **Agent** `project-reviewer` | Dipanggil oleh command/skill, atau eksplisit: "use the project-reviewer subagent" | Otak sebenar — jangan padam. Isolated context jaga main session bersih |

## Kenapa subagent + trigger nipis?
- Review baca banyak fail → kalau jalan dalam main session, context awak penuh dengan output mentah dan kualiti jawapan merosot.
- Subagent jalan dalam context window sendiri, baca semua, dan pulangkan **hanya laporan akhir** ke sesi utama.
- `tools: Read, Grep, Glob, Bash` sahaja (tiada Write/Edit) = audit read-only sebenar.
- `model: opus` sebab review strategik perlu reasoning dalam. Tukar ke `sonnet` kalau nak jimat/laju.

## Tips
- **Repeat review:** lampirkan laporan lama, tambah: "Compare against the previous review — what improved, regressed, or remains open?"
- **Multi-agent cross-check:** jalankan pada Opus dan Sonnet, banding. Finding yang muncul pada kedua-dua biasanya paling sahih.
- **Projek trading/EA awak:** seksyen security sudah ada checklist idempotency + replay protection untuk order execution — kekalkan.
- **100% tanpa soalan:** dalam `project-reviewer.md`, tukar baris Phase 0.6 kepada "Never ask questions; proceed with best inference and mark all assumptions."
