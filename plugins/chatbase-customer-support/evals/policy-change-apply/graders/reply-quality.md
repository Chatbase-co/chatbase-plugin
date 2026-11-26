---
type: llm
weight: 2
---
PASS if the reply reports what it changed (at least a new Q&A stating free shipping over $75) and what is left for the user (for example the "Shipping Policy" source and the website, which it couldn't read or change), and does not claim the new source is live without checking its status.
FAIL if it says nothing about what is left for the user, or invents an old value it never found.
