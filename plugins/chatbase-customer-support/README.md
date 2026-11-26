# Chatbase for Customer Support

Run your Chatbase AI support agent and your Chatbase help desk from Claude. Built for support leads and CX operations teams: ask in plain words and Claude does the work in your Chatbase account, showing every change before it makes it.

## What you can ask

| Job | Try |
|---|---|
| Work the ticket queue | "Go through my queue", "reply to ticket 482", "close tickets waiting on the customer for 2 weeks" |
| Weekly or monthly support report | "Write this week's support report for leadership" |
| Roll out a policy change everywhere | "Returns are now 45 days instead of 30" |
| Turn a bug cluster into one issue | "Are customers hitting the same bug?", "the checkout bug is fixed, tell everyone who reported it" |
| Fix wrong answers | "Why did the bot tell someone we ship to Brazil?", "why are so many chats reaching my team?" |
| Fill knowledge gaps | "What did customers ask this month that the bot couldn't answer?" |
| Teach the agent new facts | "We now close at 6pm", "add our new pricing from this doc" |
| Update the agent for a launch | "Update the bot from this release note" |
| Write a procedure | "Make a procedure for damaged-item claims" |
| Health check | "How is my support bot doing?" |
| Shift handoff | "Write the end-of-shift handoff" |
| Change tone or settings | "Make it friendlier", "we're closed Dec 24 to 26" |
| What customers are saying | "Any complaints about delivery this week?" |

Replies to customers are sent one at a time, each after you approve it. Deletes and overwrites always ask first.

## Install

In Claude (claude.ai, desktop, Cowork): find **Chatbase for Customer Support** in the plugin directory and install it.

In Claude Code:

```
/plugin marketplace add Chatbase-co/chatbase-plugin
/plugin install chatbase-customer-support@chatbase
```

In Codex:

```
codex plugin marketplace add Chatbase-co/chatbase-plugin
codex plugin add chatbase-customer-support@chatbase
```

## Sign in

The plugin connects to Chatbase's MCP server (`https://mcp.chatbase.co/api/mcp`) with OAuth. The first time a Chatbase tool runs you sign in to your Chatbase account and choose what the connection may do. There is no API key, and none is stored in this repository. The tools need a Chatbase plan of Basic or higher.

If you already use the Chatbase connector or the general Chatbase plugin, this plugin uses the same server; the clients de-duplicate it by name.

## Data

The plugin reads and changes data in your own Chatbase account only, through Chatbase's MCP server. It sends nothing to any other service. If you ask it to file an issue or post a report in another tool (Linear, Jira, Slack, Google Docs), it uses that tool's own connector, after you approve, and leaves customer names, emails and phone numbers out. Privacy policy: https://www.chatbase.co/legal/privacy

## Support

Docs: https://www.chatbase.co/docs. Help: the chat on https://www.chatbase.co.
