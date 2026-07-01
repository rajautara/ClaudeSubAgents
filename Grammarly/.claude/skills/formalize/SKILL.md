---
name: formalize
description: >-
  Rewrites text into a formal, professional register — for emails, reports,
  business messages, and official correspondence. Triggers when the user asks
  to "make this more formal", "formalize this", "make this sound
  professional", "tone this down for work", or "write this for a business
  email". Works in English or Japanese.
---

# Formalize

Rewrite the given text in a formal/professional register while keeping every
fact and intent intact.

## Steps

1. **Find the text** the user wants formalized (pasted, quoted, or referenced).
2. **Rewrite for formality**:
   - Remove contractions, slang, filler words, and casual interjections.
   - Replace colloquial phrasing with precise, professional vocabulary.
   - Use complete sentences and standard business/document conventions
     (proper greetings/sign-offs if it's an email, no ALL CAPS shouting,
     measured hedging instead of blunt commands).
   - In Japanese, raise the register appropriately (e.g. plain/casual form →
     です/ます, or further to keigo if the context is clearly a formal
     business or customer-facing message) — state which register you chose.
3. **Preserve substance**: every fact, request, number, and deadline in the
   original must survive. Do not soften or exaggerate claims, add hedges that
   change meaning, or remove information to "sound better."
4. **Keep length comparable** unless conciseness is itself part of sounding
   more professional — don't pad the text just to seem formal.
5. **Output** the formalized text in full. If the source was already formal,
   say so and make only minimal polish.

## Notes

- If the text is a message to a specific audience (e.g. a client vs. a
  manager), and that's stated or implied, calibrate formality to that
  audience rather than maxing it out by default.
- Don't invent a subject line, recipient, or sign-off that wasn't implied by
  the source unless the user is clearly asking to draft a full email.
