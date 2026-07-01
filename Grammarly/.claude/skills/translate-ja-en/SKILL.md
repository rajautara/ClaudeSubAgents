---
name: translate-ja-en
description: >-
  Translates text between Japanese and English, auto-detecting which
  direction is needed. Triggers when the user asks to "translate this",
  "what does this say in English/Japanese", pastes Japanese text without
  further instruction, or pastes English text and asks for a Japanese
  translation.
---

# Translate (Japanese ⇄ English, auto-detect)

Translate the given text between Japanese and English, choosing the
direction automatically unless the user states it explicitly.

## Steps

1. **Detect the source language and direction**:
   - If the user explicitly says "translate to Japanese" / "translate to
     English" / "into English" etc., follow that instruction regardless of
     what the source looks like.
   - Otherwise, auto-detect: text containing hiragana, katakana, or kanji →
     source is Japanese, target is English. Text that is essentially
     English/Romaji with no Japanese script → source is English, target is
     Japanese.
   - If the text is mixed or ambiguous, translate to whichever language is
     NOT the dominant one in the text.
2. **Translate naturally, not literally.** Prioritize fluent, idiomatic
   output in the target language over word-for-word mapping. Reorder clauses,
   drop untranslatable particles, and adapt idioms to their natural
   equivalent.
3. **Handle register deliberately**:
   - Japanese → English: don't try to preserve keigo/politeness levels
     literally (English doesn't grammaticalize them) — instead pick an
     English tone (casual / neutral / formal) that matches the source's
     social register, and briefly note the choice if it's non-obvious.
   - English → Japanese: choose an appropriate register — plain form, です/ます,
     or keigo — based on context (a message to a boss/customer defaults to
     polite/keigo; a message to a friend defaults to plain form). State which
     register was used.
4. **Preserve names, proper nouns, numbers, and technical terms** as-is
   unless there's a standard translated/localized form.
5. **Output**: the translated text first. If any phrase was ambiguous,
   idiomatic, or could be read multiple ways, add a short note below
   explaining the choice made — don't clutter the main translation with
   inline caveats.

## Notes

- For short, single-word/phrase lookups, it's fine to give 1–2 alternative
  translations if the "best" one is genuinely ambiguous (e.g. multiple
  reasonable English renderings of a Japanese term).
- Never leave part of the input untranslated because it "seemed like a proper
  noun" without checking — verify against context first.
