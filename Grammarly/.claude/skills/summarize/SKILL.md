---
name: summarize
description: >-
  Condenses text into its key points — bullet summaries, TL;DRs, or short
  abstracts. Triggers when the user asks to "summarize this", "give me a
  TL;DR", "what are the key points", "condense this", or pastes a long
  document/email/article and asks what it says. Works in English or Japanese.
---

# Summarize

Condense the given text to its essential points without losing critical
information.

## Steps

1. **Find the text** to summarize (pasted, quoted, a file, or a long block
   earlier in the conversation).
2. **Pick a length** based on the request and source length:
   - No length specified → default to a tight bullet list (3–7 bullets) for
     anything longer than a few paragraphs, or a 1–2 sentence summary for
     already-short text.
   - Explicit request ("one line", "TL;DR", "detailed summary", "executive
     summary") → honor it exactly.
3. **Preserve what matters**: names, dates, numbers, decisions, action items,
   deadlines, and conclusions must not be dropped or altered. Drop rhetorical
   flourishes, repetition, and filler — keep substance only.
4. **Don't add opinions or claims** that aren't in the source. A summary
   reports what the text says, not what the assistant thinks about it (unless
   explicitly asked for an assessment too).
5. **Output** the summary in the requested format (bullets, single paragraph,
   or one line). If the source had distinct sections, mirror that structure
   briefly rather than flattening everything into one list.
6. If the input was clearly truncated or is only part of a larger document,
   note that the summary only covers what was provided.

## Notes

- For action-item-heavy text (meeting notes, emails), separate "key points"
  from "action items / next steps" if both are present.
