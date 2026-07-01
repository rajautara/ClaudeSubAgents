---
description: Translate text between Japanese and English, auto-detecting the source language and direction.
argument-hint: "[text to translate, optionally prefixed with a direction like 'to Japanese:' ]"
---

Translate the following text between Japanese and English. Auto-detect the
source language and translate to the other one, unless the arguments state an
explicit direction (e.g. "to Japanese", "into English") — in that case follow
it regardless of the source. Translate naturally and idiomatically, not
word-for-word. Choose an appropriate register (for English → Japanese: plain
form, です/ます, or keigo, based on context) and state which one you used.
Preserve names, numbers, and technical terms.

Text:
$ARGUMENTS

If no text was provided above, use the most recently shared text or file in
this conversation. Output the translation, then a brief note on any
ambiguous or idiomatic phrase and the register choice.
