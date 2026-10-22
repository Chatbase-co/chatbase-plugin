---
name: chatbase-multi-agent
description: Compare Chatbase agents or apply one change to several — diff staging against prod, copy settings from one agent to another, add the same rule or Q&A to many agents. For agencies and teams with several bots. Use for "what's different between staging and prod", "copy staging to prod", "add this rule to all my bots".
---

# Several agents

## Compare (two rounds)

Resolve both ids with `chatbase_list_agents`, then call `chatbase_get_agent` and `chatbase_list_sources` on both agents, together. Show only the differences: setting, agent A, agent B. Sources compare by type and name (a website source's URL is its `name`); text and Q&A content can't be compared, only names and sizes.

## Copy A's setup to B

1. Let the user pick the fields. Skip agent-specific ones unless asked: name, `allowedDomains`, `creditLimit`, `notificationsSettings`.
2. Keep B's old values in the conversation for undo, then `chatbase_update_agent` on B. Send full arrays, and `channelInstructions` with all 17 channel keys (`{}` for channels with no override).
3. Re-create A's missing website sources on B with `chatbase_create_source`: `url` = A's source `name`, `linkType` and paths from A's `metadata`.
4. List what can't be copied — text and Q&A sources, files, actions, widget styles — and point to the dashboard. If the user wants everything, offer `chatbase_clone_agent` of A instead.

## One change to many agents

1. `chatbase_list_agents`; ask which ones (all, or a named subset).
2. `chatbase_get_agent` on each target, five at a time.
3. Work out each agent's own new value: append the rule to that agent's own `instructions`, skip agents that already have it, and flag ones where it conflicts with an existing rule.
4. Show one table — agent, change, note — and suggest trying it on one or two agents first.
5. On one approval, apply five at a time (`chatbase_update_agent` or `chatbase_create_source`); stop at the first unexpected error.
6. Report "changed 28 of 30" with the reason for each skip or failure.

## Ask first

The copy, per set of fields; the bulk table, once.

## Watch out

One bad rule breaks every bot at once. Keep the old values in the conversation so a revert is possible.
