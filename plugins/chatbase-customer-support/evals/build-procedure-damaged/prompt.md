---
name: build-procedure-damaged
tags: ["build-procedure"]
max_turns: 40
runs: 3
timeout_seconds: 900
append_system_prompt: "Today is Wednesday 2026-11-25, 15:00 in America/Toronto. Use this as the current date and time."
---
Make a procedure for damaged-item claims. Customers must send a photo within 7 days of delivery. If the item is under $50 we reship it; over $50 someone on the team decides.
