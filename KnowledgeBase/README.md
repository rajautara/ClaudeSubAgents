# KnowledgeBase

A Claude Code suite that turns a folder of documents into a queryable internal
knowledge base. Two subagents do the work: **`report-extractor`** converts source
documents (PDF, Word, Excel, scans) into clean, grep-friendly Markdown — one file
per report — and **`kb-expert`** answers questions strictly from those files,
never inventing. An auto-generated, index-first layout keeps lookups accurate and
cheap on context.

## Roles

| Agent | Tools | Model | Does |
|---|---|---|---|
| `kb-expert` | `Read`, `Grep`, `Glob` (read-only) | sonnet | Answers SOP / product / pricing / org questions **only** from `knowledge-base/`, citing the source file. Says so plainly when info isn't there. |
| `report-extractor` | `Read`, `Write`, `Bash`, `Grep`, `Glob` | sonnet | Extracts documents into one Markdown file per report under `extracted/`, then rebuilds the domain index. Writes only inside `extracted/` and `_raw/`. |

## Triggers

Each capability has a slash command, an auto-invoked skill, and the underlying
agent — pick whichever fits.

| Capability | Command | Skill (auto) | Agent |
|---|---|---|---|
| Look up an answer | `/kb [question]` | `kb-lookup` | `kb-expert` |
| Extract a document | `/extract [path] [domain]` | `report-extract` | `report-extractor` |

The skills fire automatically when Claude detects the intent (e.g. *"berapa harga
ar-rahnu"*, *"convert this PDF to markdown"*), so you don't have to remember the
command names.

## How it works

```
_raw/report.pdf
   │  /extract  →  report-extractor  →  scripts/extract_report.py
   ▼
raw text
   │  structured to the standard template
   ▼
extracted/<customer-slug>-<period>.md   (front-matter + clear headings)
   │  scripts/rebuild_index.py
   ▼
knowledge-base/<domain>/README.md  (auto-generated index — never hand-edited)
   │
   │  /kb "question"  →  kb-expert reads the index first, greps, then reads
   ▼                     only the 1–3 most relevant files
answer + source citation
```

- **Index-first** — agents read the master and domain `README.md` indexes before
  opening individual files, so context stays small even as the KB grows.
- **Derived indexes** — domain `README.md` files are rebuilt from the Markdown
  front-matter by `rebuild_index.py`. Never edit them by hand; re-run the script
  after adding or deleting a report.
- **Read-only by construction** — `settings.json` denies writes/edits under
  `knowledge-base/**` (and `rm`/`mv`) for the lookup path; only the extractor
  writes, and only into `extracted/` and `_raw/`.

## Layout

```
KnowledgeBase/
├── .claude/
│   ├── agents/                 # kb-expert, report-extractor
│   ├── commands/               # /kb, /extract
│   ├── skills/                 # kb-lookup, report-extract
│   ├── scripts/                # extract_report.py, rebuild_index.py, validate_kb.py
│   └── settings.json           # read-only guards on knowledge-base/**
└── knowledge-base/
    ├── README.md               # master index (domains + quick keywords)
    └── <domain>/
        ├── README.md           # domain index (auto-generated)
        ├── _raw/               # original documents — never deleted
        └── extracted/          # clean Markdown (source of truth for the index)
```

Current domains include `customer-reports`, `maa-eurodesign`,
`eskayvie-mindtropic`, `dosyien-homestay`, and `mamit` — see
[`knowledge-base/README.md`](knowledge-base/README.md) for the full map.

## Installation

Copy the `.claude/` folder to your **project root** (commit it to git to share
with your team):

```
cp -r .claude /path/to/your-project/
```

Bring your `knowledge-base/` folder alongside it (or start one — each domain just
needs a `README.md` index and an `extracted/` folder). After copying files to
disk, **restart your Claude Code session** so the agents and skills load, then run
`/agents` to confirm.

For extraction, install the toolchain on first use:

```
pip install pdfplumber python-docx openpyxl pandas
# OCR for scanned PDFs/images (optional):
#   apt-get install -y tesseract-ocr poppler-utils  →  pip install pytesseract pdf2image
```

## Scripts

| Script | Purpose |
|---|---|
| `extract_report.py <file>` | Pull text/tables out of a PDF/Word/Excel/image source |
| `rebuild_index.py <domain>` | Regenerate a domain `README.md` index from the Markdown front-matter |
| `validate_kb.py <domain>` | Flag drift — orphan Markdown, unprocessed `_raw/`, missing front-matter |

## Usage examples

```
/kb berapa harga buyback emas lama untuk MAA EuroDesign?
/kb what is the Ar-Rahnu workflow?
/extract ./inbox/acme-q1.pdf customer-reports
```

Or just describe the intent and let the skills route it: *"convert these customer
reports to markdown"* → `report-extract`; *"what's our shipping SOP for
Eskayvie?"* → `kb-lookup`.
