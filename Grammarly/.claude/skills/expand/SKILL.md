---
name: expand
description: >-
  Expands short notes, outlines, or draft text into fuller, more detailed
  prose while keeping the original ideas and voice. Triggers when the user
  asks to "expand this", "flesh this out", "make this longer", "elaborate on
  this", or "turn these notes/bullets into full sentences/paragraphs". Works
  in English or Japanese.
---

# Expand

Turn short notes, bullets, or a terse draft into fuller prose without
inventing new claims.

## Steps

1. **Find the source text** — notes, an outline, bullet points, or a short
   draft the user wants expanded.
2. **Expand structurally, not just verbally**:
   - Turn bullets/fragments into complete sentences and paragraphs.
   - Add transitions, connective tissue, and reasonable supporting detail
     (examples, context, elaboration on a stated point).
   - Keep the original order and emphasis of ideas — expansion fills gaps
     between the given points, it doesn't reorganize or reprioritize them.
3. **Don't invent facts.** Only add detail that is a reasonable, clearly
   -implied elaboration of what's already there (e.g. spelling out an
   example the note gestures at). If you add anything that's a genuine
   assumption rather than an implication, flag it explicitly (e.g. "assuming
   this refers to X — adjust if not").
4. **Match the original voice and tone** — a casual note stays casual when
   expanded; a formal outline stays formal.
5. **Output** the expanded text in full. If the user gave a target length
   (e.g. "make it a full paragraph", "expand to ~300 words"), hit that
   target; otherwise expand to a natural, complete version of what the notes
   were gesturing at — don't pad with filler just to add length.

## Notes

- If the input is extremely terse (a few words) and genuinely underspecified,
  ask one clarifying question about direction/audience rather than guessing
  wildly and inventing content.
