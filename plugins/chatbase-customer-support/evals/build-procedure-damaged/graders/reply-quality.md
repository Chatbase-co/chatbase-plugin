---
type: llm
weight: 2
---
PASS if the reply shows a draft procedure with a trigger about damaged items, steps that ask for the order and a photo, check the 7-day window, branch on under $50 (reship) versus over $50 (hand off to the team with the create_ticket action, no promised outcome), and asks for approval before creating it. It may note that reshipping needs an action the agent doesn't have.
FAIL if it says the procedure was created, or the over-$50 path promises a refund or replacement.
