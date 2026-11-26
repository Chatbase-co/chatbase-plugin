---
type: llm
weight: 2
---
PASS if the reply flags the wrong promises first (25% off for a 3-year commitment in conv_disc1, and "annual billing saves 20%" if found), identifies dead-end answers about CrewPilot (comparisons and importing job history), notes the weak answer to "CrewPilot is $29, why are you $49", and asks the user for the facts before drafting answers.
FAIL if it drafts competitor claims or discounts the user never gave, or misses the 25% promise.
