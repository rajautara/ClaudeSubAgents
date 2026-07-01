# Grammarly — Claude Code Setup

A small writing-assistant toolkit for Claude Code: five text-editing
capabilities, each available both as a slash command (explicit) and as an
auto-invoked skill (Claude decides when to use it).

## Structure

```
.claude/
├── commands/
│   ├── fix-grammar.md      # /fix-grammar [text]
│   ├── formalize.md        # /formalize [text]
│   ├── summarize.md        # /summarize [text]
│   ├── translate.md        # /translate [text]
│   └── expand.md           # /expand [text]
└── skills/
    ├── fix-grammar/SKILL.md
    ├── formalize/SKILL.md
    ├── summarize/SKILL.md
    ├── translate-ja-en/SKILL.md
    └── expand/SKILL.md
```

There are no subagents here on purpose — these are lightweight, in-context
text transforms. The result should show up directly in the conversation, not
get summarized back from an isolated context.

## Installation

Copy the `.claude/` folder to your **project root** (project scope — commit
it to git to share with your team):

```
cp -r .claude /path/to/your-project/
```

Or place it in `~/.claude/` (user scope) to use it across **all** projects.
After copying, **restart your Claude Code session** so the files are loaded
(skills/commands added directly to disk require a restart).

## The five tools

| Command | Skill | What it does |
|---|---|---|
| `/fix-grammar` | `fix-grammar` | Corrects grammar, spelling, and punctuation errors only — no style rewrites. |
| `/formalize` | `formalize` | Rewrites text into a formal/professional register (email, report, business message). |
| `/summarize` | `summarize` | Condenses text into key points — bullets, TL;DR, or a short abstract. |
| `/translate` | `translate-ja-en` | Translates between Japanese and English, auto-detecting the direction. |
| `/expand` | `expand` | Expands short notes/outlines into fuller, detailed prose. |

## When to use which

- **Command** (`/fix-grammar`, `/formalize`, ...): when you want a specific
  transform right now, with an explicit trigger. Pass the text as an
  argument, e.g. `/formalize can u send this over asap thx`, or leave it
  blank to have Claude use the text already in the conversation.
- **Skill**: triggers automatically when Claude detects the intent — e.g.
  pasting a paragraph and asking "does this sound okay?", or pasting
  Japanese text with no further instruction (which the `translate-ja-en`
  skill picks up and translates to English).

## Tips

- **Chain them**: e.g. `/expand` a rough note, then `/formalize` the result
  for an email, then `/fix-grammar` as a final pass.
- **Translate is direction-agnostic**: just paste Japanese or English text
  and it detects which way to go. To force a direction, say so explicitly
  (e.g. "translate to Japanese: ...").
- **`fix-grammar` vs `formalize`**: use `fix-grammar` when the text is
  already the right tone and just needs correcting; use `formalize` when the
  tone itself needs to change (casual → professional).
- All five skills work on English or Japanese text; the other tools
  (fix-grammar, formalize, summarize, expand) aren't limited to those two
  languages — they follow whatever language the input is in.
