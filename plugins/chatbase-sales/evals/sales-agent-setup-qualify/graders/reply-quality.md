---
type: llm
weight: 2
---
PASS if the reply, before changing anything, proposes: instruction changes that ask qualifying questions and offer the lead form or a demo when visitors ask about Enterprise pricing; a better whenToUse for collect_leads (not only "when the visitor asks to be contacted"); starter questions such as "Book a demo"; and a qualification procedure that uses @collect_leads and @book_demo. It notes that Chatbase can't see whether a demo was actually booked, and asks for approval.
FAIL if it says changes were already applied, invents pricing or discount rules, or misses that collect_leads only fires when asked to be contacted.
