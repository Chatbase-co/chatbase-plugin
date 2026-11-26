---
type: llm
weight: 2
---
PASS if the reply starts with counts (about 61 owed a reply, 14 unassigned, 5 urgent or high), then lists the urgent or high tickets (including #1060 "Order 88213 never arrived", urgent and unassigned, and #1061 "Charged twice"), then unassigned ones oldest first, with ages; and offers a next step.
FAIL if counts are missing or contradict those numbers, or it presents one page as the whole queue.
