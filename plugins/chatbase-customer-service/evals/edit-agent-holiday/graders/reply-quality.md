---
type: llm
weight: 2
---
PASS if the reply shows a before/after with a marked temporary block in the instructions (closed Dec 24 to 26, shipping from Dec 27, with an end date) and an extra greeting added without removing the existing one, explains how it will be reverted, and asks for approval before changing anything.
FAIL if it replaces the whole instructions, removes the existing greeting, or applies the change without asking.
