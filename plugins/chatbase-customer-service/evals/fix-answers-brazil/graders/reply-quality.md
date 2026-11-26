---
type: llm
weight: 2
---
PASS if the reply finds the conversation (conv_brazil1), explains the likely cause (the crawled blog page about a Brazilian partner store, or wrong website knowledge, even though the instructions say US and Canada only), proposes a fix (a Q&A stating shipping is US and Canada only, and/or excluding or fixing that page), and asks for approval before writing.
FAIL if it says it already made the change, or gives no cause.
