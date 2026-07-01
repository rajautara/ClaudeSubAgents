---
name: fix-grammar
description: >-
  Corrects grammar, spelling, punctuation, and word-usage errors in text while
  preserving the original meaning, tone, and voice. Triggers when the user
  asks to "fix my grammar", "proofread this", "check my spelling", "does this
  sound right", or pastes a sentence/paragraph/email and asks for corrections.
  Works in English or Japanese.
---

# Fix Grammar

Correct errors in the given text without rewriting its style or intent.

## Steps

1. **Find the text.** Use whatever the user pasted or referenced in this
   message. If they pointed at a file, read only the relevant section — don't
   touch code, config, or non-prose content unless explicitly asked.
2. **Fix only real errors**: grammar, spelling, punctuation, subject-verb
   agreement, tense consistency, article/preposition misuse, and word choice
   that is factually wrong (e.g. "affect" vs "effect"). Do not change tone,
   register, sentence structure, or vocabulary beyond what's needed to fix the
   error — this is proofreading, not rewriting.
3. **Preserve formatting**: line breaks, lists, headings, emphasis, and any
   code/inline-code spans must stay untouched.
4. **Output:**
   - The corrected text in full, ready to copy-paste.
   - If changes were made, a short list below it: `original → corrected` with
     a one-line reason for each non-obvious fix. Skip this list if there's
     only one trivial fix.
   - If no errors were found, say so plainly instead of inventing changes.

## Notes

- If the text is ambiguous between two valid readings, pick the one that
  best fits context and flag the ambiguity briefly rather than silently
  guessing.
- Never "correct" stylistic choices (contractions, sentence fragments used
  for effect, casual tone) that aren't actually errors.
