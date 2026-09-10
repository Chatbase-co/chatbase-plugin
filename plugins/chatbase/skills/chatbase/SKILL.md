---
name: chatbase
description: Use when managing Chatbase agents, sources, conversations, or help-desk tickets through the Chatbase MCP server
---

# Chatbase MCP

Judgment the tool schemas can't express. Read this before calling any tool below.

## Resolve `agentId` — never guess it

`agentId` is an opaque id, not the agent's display name. Call `chatbase_list_agents` first, match the target by `name`, and use the id it returns. Never construct, infer, or reuse an id from memory or from another agent's id.

## Sources train on write — there is no train step

- Creating, updating or deleting a source takes effect on the agent's knowledge **immediately**. There is no separate training step and no tool to trigger one: the work starts the moment you write.
- A new source comes back `untrained` and flips to `trained` once it is live, or `failed` if it did not land. An edited source shows `updated` until it is live again. Call `chatbase_get_source` to follow one, or `chatbase_get_agent` for the agent-level `status`. Do not report a source as live because the write succeeded — the write only means the work started.
- **Deleting a source is immediate and permanent.** The knowledge is purged straight away; the source comes back `deleted`, or `toBeDeleted` while the purge finishes. Nothing restores it — there is no undo and no recovery tool. Confirm with the user before every `chatbase_delete_source`, and say plainly that it cannot be undone. Re-creating the source afterwards is a new source that has to train again from scratch.
- Editing a source overwrites its content and retrains it on the spot, so the previous text and everything learned from it are gone. Treat `chatbase_update_source` as destructive too: confirm before overwriting content the user may not have a copy of.

## Conversations: `chatbase_export_conversations` only

- This is the **only** source-complete conversation reader on this server. There is no `listConversations`, `getConversation`, or `listConversationMessages` tool — they were deliberately left out because those API operations silently return API-source conversations only, making widget and WhatsApp conversations invisible. Never conclude "no conversations exist" from anything but export.
- `include` defaults to `summary` (message bodies omitted). Only switch to `include: 'messages'` for a conversation you've already picked out for full reading, one or a few `conversationId`s at a time — not as the first pass over a page.
- Bulk analysis over many conversations is MCP work. Do it well:
  - Stay in `include: 'summary'` for the sweep — it omits message bodies and is the cheap mode.
  - Page with `pagination.cursor` until `hasMore` is false, aggregating findings as you go rather than accumulating raw pages in context.
  - `chatbase_export_conversations` returns at most **20 conversations per call**, so a large sweep is many sequential calls. Before starting a long one, tell the user roughly how many pages to expect, and report partial findings as you go rather than going silent until the end.
  - Only escalate a specific conversation to `include: 'messages'` once the summary shows it matters.
  - The general pagination-discipline rule below ("read one page and stop unless asked") still governs exploratory reads — an explicit bulk-analysis request is the case where paging through everything is the correct behaviour.

## `chatbase_chat` writes to the customer's live data

`chatbase_chat` is not a test harness. Every call starts or continues a **real conversation** on a real agent: it consumes the account's credits, and the exchange appears in the customer's conversation logs alongside genuine end-user traffic, where it can distort what their analytics and exports show.

- Never call it to check that the connection works or that an agent exists. Use `chatbase_whoami` for connectivity and `chatbase_get_agent` to confirm an agent.
- Call it when the user has actually asked you to talk to an agent, and say which agent you are messaging before you do.
- Pass `conversationId` to continue a thread. Omitting it starts a new conversation every time, so a multi-turn exchange without it leaves a trail of one-message conversations in their logs.
- Streaming is not available here; the full reply always arrives in one response.

The reply may contain `tool-call` and `tool-result` parts from actions the agent ran, carrying internal identifiers — `toolCallId`, and widget `state.id` / `actionId`. Read them if they help you answer, but summarise what the agent did in plain language. Do not quote those ids back to the user, and never write them into a ticket reply or a file.

`chatbase_update_conversation` pauses or resumes a live conversation. Pausing stops the agent replying to a real person who may be mid-conversation, so confirm with the user before calling it, and say which conversation you are changing.

## Pagination discipline

- Read one page, report what's in it, and stop. Never loop pages to "get everything" unless the user asked for that.
- `pagination.hasMore: true` is the primary "more exists" signal — every paginated response carries it, so check it first. It means more items exist; say so explicitly rather than presenting a page as the complete list.
- `truncated: true` is a rarer backstop that only appears when a tool's own cap silently cut a page short (it can't fire when the request already asked for at most the cap). Treat it the same way as `hasMore: true` when you do see it.
- On `chatbase_search_tickets`, `hasMore: true` with a null `cursor` means there's no page to fetch — narrow the query instead of looking for a way to page.

## When a result is not the whole answer

Several tools return something that is only meaningful once you fetch the rest, or resolve an id. Finish the job rather than handing the user a fragment.

- **A cursor is an instruction, not decoration.** `pagination.cursor` with `hasMore: true` means the answer you have is partial. If the user asked a question the page cannot answer — "how many", "which one", "any that…" — keep paging with that cursor until `hasMore` is false before answering. If you stop early, say how much you read: "the newest 25 of at least 60".
- **Never answer a counting or superlative question from one page.** "Which agent has the most sources", "how many tickets are open", "the oldest conversation" — all require the full set. One page gives you the top of a list, not a maximum.
- **Ids are not answers.** A result carrying `agentId`, `sourceId`, `statusId`, `authorId` or `conversationId` and no name is not yet usable by a person. Resolve it — `chatbase_get_agent`, `chatbase_get_source`, `chatbase_list_ticket_statuses`, `chatbase_list_helpdesk_teams` — and report the name, keeping the id only if the user needs it to act.
- **A summary is a filter, not a reading.** `chatbase_export_conversations` in its default `summary` mode omits message bodies. Answering "what did people ask about" from summaries alone is guessing; use the summaries to choose which conversations matter, then re-read those few with `include: 'messages'`.
- **A ticket without its messages is half a ticket.** `chatbase_get_ticket` returns the record; the conversation lives in `chatbase_list_ticket_messages`. Summarising a ticket means reading both.
- **A write result is a receipt, not a state.** `{"success": true}` confirms the call was accepted, not what the record now looks like. When the user needs to see the outcome, re-read it — `chatbase_get_ticket`, `chatbase_get_agent`, `chatbase_get_source` — and report actual state.
- **`chatbase_get_sources_summary` is counts, not content.** Use it to see how much a knowledge base holds; use `chatbase_list_sources` when the user needs to know what is in it.

Chain the calls yourself. Asking the user to run a second query you could have run is the failure this section exists to prevent.

## Confirm before destructive tools

Ask the user before calling any of:
- `chatbase_delete_agent`
- `chatbase_delete_source` — the purge is immediate and there is no way back.
- `chatbase_update_source` — a content change overwrites the source and retrains it at once, discarding the previous text and its embeddings. It does not "delete" anything by name, which is exactly why it is easy to under-estimate.

## Error-code playbook

- `RATE_LIMIT_TOO_MANY_REQUESTS` — back off and honour any retry-after; never retry in a tight loop.
- `SUBSCRIPTION_API_RESTRICTED_PLAN` — stop and tell the user which plan the operation requires.
- `AGENT_NOT_FOUND` and a plain 403 are both tenant-scoping failures — the id isn't wrong, it isn't yours. Do not retry with a different guessed id; re-resolve via `chatbase_list_agents`.
- `CHAT_CONVERSATION_NOT_ONGOING` — the conversation ended; start a new one instead of retrying the same `conversationId`.
- `SOURCE_PENDING_DELETION` — the source is mid-purge and cannot be edited. It is not recoverable: create a new source instead of waiting for it to come back.
- `SOURCE_IS_TRAINING` — a training run owns the source right now, so the edit would be overwritten by the run's own write. Wait and retry the edit; deleting is still allowed.
- 5xx from `chatbase_update_ticket` — do not assume the update was rejected. Fields are validated together but written independently, so some may have applied. Re-read with `chatbase_get_ticket` and report actual state before retrying; never retry the whole payload blind.

## Ticket attachments

`chatbase_list_ticket_messages` returns `attachments` as `{name, url, type, size}`. The file is fetchable — retrieve it yourself instead of telling the user to go to the dashboard or CLI.

- Fetch `url` with a plain HTTP GET and **no `Authorization` header**. The route is unauthenticated by design — the token embedded in the URL path is itself the credential. Do **not** add one: the route ignores it, so it does not fail loudly — it just means you transmitted your OAuth access token to a route that never needed it, and on to the storage host it redirects to.
- The request 302-redirects to a short-lived (120s) signed URL. Follow the redirect and read the body in the same request; do not save the redirect target to fetch later, since it will have expired.
- The **token URL itself does not expire.** Treat it as a durable secret, not a throwaway link: fetch it only when you need the content, never repeat it back in your own output, and never write it into a file or a ticket reply.
- `name`, `type`, and `size` may be `null`; don't assume a filename or MIME type exists before using one.
- `attachments` is always an empty array on `event` messages — don't expect files there.
- After `chatbase_create_ticket_message` succeeds, tell the user the reply was recorded, not delivered — and re-read with `chatbase_get_ticket` rather than assume its status is unchanged.

## Chatbase tickets, not third-party tickets

Every `chatbase_*_ticket*` tool operates on **Chatbase's own help desk only**. Chatbase can integrate with third-party ticketing platforms (Zendesk, Intercom, etc.), but neither this MCP server nor the CLI can read or write tickets in them. Never present a Chatbase helpdesk result as if it covers a customer's third-party platform, and if the user asks about one, say plainly that it isn't reachable from here.

## When a tool seems missing

Call `chatbase_whoami` first. A short tool list almost always means a narrowly-scoped OAuth grant, not an absent capability.

## Capabilities that live in the CLI, permanently

Absence from this tool surface is not absence of the capability — point the user at the CLI. These are permanent CLI-only capabilities:
- File-source upload — `chatbase sources create --file <path> -a <agentId>` / `chatbase sources update <sourceId> --file <path>`. A remote MCP server has no filesystem to read from.
- `updateAgentStyles` — `chatbase agents styles <agentId> --data '<json>'`.
- WhatsApp template send — `chatbase whatsapp send-template <name> --to <phone> -a <agentId>` — sends a real message with no delivery confirmation, so keep it at a human's terminal.
- WhatsApp template list — `chatbase whatsapp templates -a <agentId>` is CLI-only alongside the send operation.

## The API is the final validation authority

The schema catches shape and cross-field rules before a request is ever sent — for example, `chatbase_update_ticket` rejects giving both `statusId` and `statusCategory`, and `chatbase_create_ticket_message` rejects giving neither, or both, of `authorId` / `authorEmail`. A schema rejection names the rule directly.

The API catches what no schema can express:
- Whether a referenced id actually exists and belongs to this account — a well-formed `statusId`, `agentId`, or `sourceId` can still be rejected as not found. That's tenant scoping, not a malformed argument.
- Plan and quota limits (`SUBSCRIPTION_API_RESTRICTED_PLAN`, rate limits, credit limits).
- State-dependent rules — a conversation that has ended (`CHAT_CONVERSATION_NOT_ONGOING`), a source being purged (`SOURCE_PENDING_DELETION`) or mid-training (`SOURCE_IS_TRAINING`).

Treat any rejection as a real constraint to satisfy, not a transient failure to retry unchanged: if the schema rejected the call, its message names the rule to fix; if the API rejected it, re-check the ids and the account's state rather than the argument shape.
