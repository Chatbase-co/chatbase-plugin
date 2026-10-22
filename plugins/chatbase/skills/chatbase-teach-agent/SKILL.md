---
name: chatbase-teach-agent
description: Teach a Chatbase agent new or changed facts from the chat, a file, or a document the assistant can open — drafts Q&A and text sources, adds them after approval, and checks the bot uses them. Use for "we now close at 6pm", "train it on this PDF", "add our new pricing". Not for fixing answers found in conversations (use chatbase-fix-answers) or changing tone (use chatbase-edit-agent).
---

# Teach the agent

## Round 1 (together)

- `chatbase_get_agent`: does `instructions` contain the fact, or its old value?
- `chatbase_list_sources` with two or three `name` filters for likely overlaps ("pricing", "hours", "faq").
- For a changed fact only: `chatbase_search_conversations` with `query` = the old value and `updatedAfter` = 30 days ago, to show how often the bot said it.

For a file or document, read it with your own file tools. For a large one, work section by section and say what you covered.

## Drafting rules

- Short facts become Q&As: a short `name` ("FAQ: store hours"), 3 to 6 phrasings a customer would use (at most 50) and an answer that stands alone ("Our store is open 9am to 6pm", not "9 to 6").
- Long guides and policies become text sources, one per topic, each with a clear `name` under 100 characters and headings inside. Focused sources retrieve better than one giant source.
- Tables become Q&As for the key rows, or a text source with one line per row.
- Skip marketing copy, boilerplate and anything without facts. At most about 15 sources per batch.

## Changed facts

- **In the instructions:** show before/after; on approval, `chatbase_update_agent` with the full new `instructions` string.
- **In a text or Q&A source:** source text can't be read, so name the likely source. Replace it with `chatbase_update_source` only if the user pastes the full new text; otherwise add the new Q&A and tell the user which source to fix in the dashboard.
- **On their website:** the site has to be fixed first. A single-page link re-scrapes on `chatbase_update_source` when the call sends a field (send `slowScraping: false`; it has no effect on a single page). A crawled or sitemap site only re-crawls when its `excludePaths` or `includeOnlyPaths` change, so for a plain refresh offer weekly auto-retrain (`chatbase_update_agent_auto_retrain`, needs the Standard plan and a trained agent) or a retrain from the dashboard.

## Approve and write

Show the source titles and two or three sources in full; one approval covers the batch. Then `chatbase_create_source`, five at a time.

## Verify

- `chatbase_get_source` once on each new source. Use the source's own `status`, not the agent's: the agent stays `failed` while any older source has failed. If one is still `untrained`, say so and stop.
- Offer to `chatbase_chat` one or two test questions (costs credits, shows in the logs) and show the answers.

## Report

What was added, and what the user still has to fix by hand.

## Ask first

The batch of new sources; every `chatbase_update_source` or `chatbase_delete_source`; instruction changes; test chats.
