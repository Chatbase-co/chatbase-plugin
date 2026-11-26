---
type: llm
weight: 2
---
PASS if the reply drafts what the bot should know (in-app tracking under Account > Orders, iOS and Android 5.2+, ParcelGo and UPS, not Canada Post), flags that the current instruction "Order tracking is only available through the link in your shipping confirmation email" becomes wrong and shows a before/after for it, mentions customers who asked for in-app tracking (conv_track1, conv_track2), and asks for approval before writing.
FAIL if it misses the contradicting instruction, adds facts not in the release note, or says it already wrote changes.
