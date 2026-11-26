# Chatbase for Sales

Turn the Chatbase agent on your website into pipeline, from Claude. Built for sales, SDR and RevOps teams: ask in plain words and Claude reads your leads and the conversations behind them, then works with the CRM, Slack, email and calendar tools you already connected to Claude. Every change and every message is shown to you before it happens.

## What you can ask

| Job | Try |
|---|---|
| Daily lead digest | "Who are today's leads worth following up?" |
| Hand a hot lead to a rep | "Priya from Acme looks hot, hand her to Sam with the context" |
| Prep for a call | "I have a call with Marcus from Northgate in an hour, prep me" |
| Follow up from the chat | "Draft a follow-up email to Dana from what she asked the bot" |
| Buying signals | "Which visitors this week showed buying intent?" |
| Objections the bot handles badly | "Where is the bot losing deals on pricing or competitors?" |
| Set the bot up to qualify and book | "Make our bot qualify visitors and book demos" |
| Weekly pipeline report | "How many leads did the bot bring in this week vs last?" |
| What buyers ask | "What are prospects asking about the enterprise plan?" |
| Create or change the agent | "Make a bot for our new landing page", "add a Book a demo starter question" |

Nothing is sent to a prospect, posted in Slack or written to your CRM without your approval, one item at a time.

## Install

In Claude (claude.ai, desktop, Cowork): find **Chatbase for Sales** in the plugin directory and install it.

In Claude Code:

```
/plugin marketplace add Chatbase-co/chatbase-plugin
/plugin install chatbase-sales@chatbase
```

In Codex:

```
codex plugin marketplace add Chatbase-co/chatbase-plugin
codex plugin add chatbase-sales@chatbase
```

## Sign in

The plugin connects to Chatbase's MCP server (`https://mcp.chatbase.co/api/mcp`) with OAuth. The first time a Chatbase tool runs you sign in to your Chatbase account and choose what the connection may do. There is no API key, and none is stored in this repository. The tools need a Chatbase plan of Basic or higher. For lead data, grant the leads permission when you connect.

## Data

The plugin reads and changes data in your own Chatbase account only, through Chatbase's MCP server. It sends nothing to any other service by itself. When you ask it to update a CRM, post in Slack or draft an email, it uses that tool's own connector in Claude, after you approve each item. Privacy policy: https://www.chatbase.co/legal/privacy

## Support

Docs: https://www.chatbase.co/docs. Help: the chat on https://www.chatbase.co.
