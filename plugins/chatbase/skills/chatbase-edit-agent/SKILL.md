---
name: chatbase-edit-agent
description: Change how a Chatbase agent behaves or is configured — tone, language, rules, per-channel instructions, greeting and starter questions, temporary notices like holidays, model, security and cost limits, voice settings. Always shows the change before applying it. Use for "make it friendlier", "reply in Arabic", "we're closed Dec 24 to 26", "stop spam", "cap my credits", "switch the model".
---

# Edit the agent

One read, one write, one re-read.

## Steps

1. `chatbase_get_agent`.
2. Map the request to fields:

| Request | Field |
| --- | --- |
| Tone, language, rules, what never to say | `instructions` |
| One channel only ("shorter on WhatsApp") | `channelInstructions` — send all 17 channel keys: stored overrides kept, `{}` for channels with none (never `""`, which blanks that channel). The override itself is a string, or `{"chat": "...", "voice": "..."}`. Keys: `chat_widget`, `help_page`, `center_stage`, `side_panel`, `slack`, `whatsapp`, `messenger`, `instagram`, `salesforce`, `zendesk`, `zendesk_messaging`, `api`, `email`, `android_sdk`, `ios_sdk`, `phone`, `search` |
| Greeting, starter questions | `initialMessages`, `suggestedMessages` — send the full arrays |
| Add or remove one allowed domain or blocked country | `allowedDomains`, `blockedCountries` — send the full arrays with the existing entries kept |
| Model, creativity | `model`, `temp` |
| Bot used on someone else's site, spam, one user flooding, regions, spend | `allowedDomains`, `spamSettings`, `ipRateLimits`, `blockedCountries`, `creditLimit` |
| Voice | `voiceSettings` (merged into the current settings) and the `voice` values in `channelInstructions` |

3. Draft the smallest change. Every other rule stays word for word; don't turn three lines into an essay. `instructions` holds at most 30,000 characters.
4. Show before/after of the changed lines only, and keep the full old value in the conversation so the user can undo.
5. On approval, `chatbase_update_agent` with only those fields, then `chatbase_get_agent` once to confirm.
6. Offer one to three test questions with `chatbase_chat` (costs credits, shows in the logs).

## Temporary notices

The revert has to work in a later conversation that remembers nothing of this one:

- Add the notice to `instructions` as one marked block, e.g. `[Temporary until 2026-12-27] The store is closed Dec 24 to 26; orders ship from Dec 27.`
- Add one greeting at the start of `initialMessages` instead of replacing the existing ones.
- To revert, remove only the marked block and that greeting; keep every other edit made since.

If you can schedule tasks, schedule the revert. Otherwise give the end date and tell the user to say "end holiday mode".

## Security and cost

- `allowedDomains` needs both `example.com` and `www.example.com`; a missing one breaks the widget for real customers.
- Show `creditsUsed` (this month) next to any new `creditLimit`. The bot stops answering at the limit.
- Blocking a country blocks everyone there.
- Setting `visibility` to `private` takes the bot offline for the public: confirm twice.

## Model switch

Offer three test questions before and after on the live agent. For a big agent, offer to test on a copy (`chatbase_clone_agent`) first: warn that the copy retrains every source before it answers (minutes), uses an agent slot and doubles the credits, and offer to delete it after with `chatbase_delete_agent`.

## Ask first

Every change, with before/after.
