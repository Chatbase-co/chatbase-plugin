# Chatbase MCP Plugin

Manage Chatbase agents, sources, conversations, and help-desk tickets from your editor, via the
Model Context Protocol.

## Plugins

| Plugin | For | What it adds |
|---|---|---|
| `chatbase` | Anyone using Chatbase from an editor | The Chatbase MCP server and general skills for agents, sources, conversations and the help desk |
| `chatbase-customer-support` | Support and CX teams | Help desk queue and replies, fixing wrong answers, policy changes everywhere, bug clusters, knowledge gaps, procedures, launch updates, shift handoffs and a weekly support report |
| `chatbase-sales` | Sales, SDR and RevOps teams | Lead digest, hot-lead handoffs, call prep, follow-up drafts, buying signals, objections, qualification and booking setup, and a weekly pipeline report |

All three use the same MCP server (`https://mcp.chatbase.co/api/mcp`). Install the one that fits; replace `chatbase@chatbase` below with `chatbase-customer-support@chatbase` or `chatbase-sales@chatbase`.

## Install

### Claude Code

```
/plugin marketplace add Chatbase-co/chatbase-plugin
/plugin install chatbase@chatbase
```

### Codex

```
codex plugin marketplace add Chatbase-co/chatbase-plugin
codex plugin add chatbase@chatbase
```

Both platforms read the same `plugins/chatbase/.mcp.json` server definition.

### Already have a `chatbase` MCP server configured manually?

If a server named `chatbase` is already configured at the same URL — Claude Code and Codex
alike — installing this plugin will not add a second entry. Clients de-duplicate server
definitions by name, so the pre-existing manual entry silently wins and the plugin's own
definition is never used. There's no error; it just looks like the install did nothing. Remove
the existing manual `chatbase` entry first, then install the plugin.

## Authentication

Authentication is **OAuth** — you'll be prompted to sign in to your Chatbase account the first
time a tool from this plugin is used. There is no API key or token to configure, and none is
shipped in this repository.

## Evals

`chatbase-customer-support` and `chatbase-sales` ship an eval suite in `evals/` for `claude plugin eval`
(Claude Code 2.1.269 or later). The cases run against a fictional company played by a mock Chatbase
server, so they need no Chatbase account and spend no credits:

```
cd plugins/chatbase-customer-support
claude plugin eval . --runs 1 --ablation none --no-publish --max-cost-usd 10
```

`evals/cases.py` is the source for the case folders (`scripts/evals/write_cases.py`). The mock tools in
`evals/mocks/chatbase/_tools.json` are generated from the API v2 spec with `scripts/evals/gen_mcp_tools.py`.
