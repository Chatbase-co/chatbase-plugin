# Chatbase MCP Plugin

Manage Chatbase agents, sources, conversations, and help-desk tickets from your editor, via the
Model Context Protocol.

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
