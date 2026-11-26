---
type: llm
weight: 2
---
PASS if the reply, before changing anything, lists the places the 30-day rule lives and how each changes: the agent instructions line; the "Start a return" procedure (its 30-day step and branch); the return sources ("Returns & Exchanges Policy", "FAQ: return window"), saying their text can't be read and offering a new Q&A or a pasted replacement; and the start_return action, whose own return-window setting the user must change in the dashboard (its whenToUse text can be updated here). It asks for approval before applying.
FAIL if it claims to have already made changes, skips the procedure or the action, or claims to know what the sources say.
