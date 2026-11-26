# The account: Trailhead Supply (fictional test company)

Today is Wednesday 2026-11-25, 15:00 America/Toronto. Trailhead Supply is an online outdoor-gear store (website trailheadsupply.com plus an iOS and Android app). It ships to the US and Canada only.

## whoami
userId `usr_maya01`, teamName "Trailhead Supply", plan "Standard", scopes: all read, write and delete scopes except `chatlogs:delete`, `agents:delete`. (whoami has no email.)

## Agents (chatbase_list_agents)
1. id `agt_trail_support`, name "Trailhead Support", status `trained`, model `gpt-5.5`, autoRetrain true, lastTrainedAt 2026-11-20, lastMessageAt 2026-11-25T19:40:00Z, visibility `public`, creditLimit 20000, creditsUsed 11240.
2. id `agt_trail_staging`, name "Trailhead Support (staging)", status `trained`, lastMessageAt 2026-11-02, creditsUsed 310, creditLimit 1000.
Any other agentId → error `AGENT_NOT_FOUND`.

## Trailhead Support: settings (chatbase_get_agent)
- instructions:
  "You are Trailhead Supply's support assistant. Be friendly and brief.\n- We ship to the US and Canada only.\n- Returns are accepted within 30 days of delivery for unused items. Start a return with the start_return action.\n- Order tracking is only available through the link in your shipping confirmation email.\n- Never promise refunds; hand refund disputes to the team with create_ticket.\n- If you don't know, say \"I don't have information on that\" and offer to connect the customer with our support team."
- channelInstructions: `whatsapp`: "Keep answers under 3 sentences."; every other channel `{}`.
- initialMessages: ["Hi! I'm Trailhead's assistant. How can I help with your gear today?"]; suggestedMessages: ["Where is my order?", "Start a return", "Sizing help"].
- allowedDomains ["trailheadsupply.com","www.trailheadsupply.com"], temp 0.2.

## Sources (chatbase_list_sources; name filter = case-insensitive substring)
- `src_site` link crawl https://trailheadsupply.com, trained, 214 pages (children.failed 0).
- `src_returns` text "Returns & Exchanges Policy", trained.
- `src_faq_return` qna "FAQ: return window", trained.
- `src_shipping` text "Shipping Policy", trained.
- `src_sizing` text "Sizing guide: boots and jackets", trained.
- `src_warranty` qna "FAQ: warranty claims", trained.
Source text can't be read through the API (get_source returns metadata only).

## Procedures (chatbase_list_procedures / get_procedure)
- `proc_return` "Start a return", enabled, trigger "The customer wants to return or exchange an item". Steps: [instruction "Ask for the order number and the email on the order."], [instruction "Check the delivery date: returns are accepted within 30 days of delivery."], [branch: condition "Delivered within the last 30 days" → steps [instruction "Call @start_return"]; otherwise → steps [instruction "Explain the 30-day window and offer to connect them with the team using @create_ticket"]].
- `proc_warranty` "Warranty claim", enabled, trigger "The customer says a product failed or broke during normal use". Steps: ask for order number and photos; call @create_ticket.

## Actions (chatbase_list_actions / get_action)
- `act_ticket` name `create_ticket`, type `create-ticket`, enabled.
- `act_live` name `live_chat`, type `chatbase-live-chat`, enabled.
- `act_return` name `start_return`, type `shopify-create-return`, enabled, whenToUse "When the customer wants to return an unused item delivered within 30 days." (its return-window setting is not returned by the API: "Other configuration is not included").
- `act_order` name `get_order`, type `shopify-show-order`, enabled.

## Analytics (chatbase_get_agent_analytics), 7 buckets summed
- 2026-11-18 → 2026-11-24 (this week): conversations 1,240; escalated 186; thumbsUp 212; thumbsDown 58; positive 0, neutral 0, negative 0 (no advanced analytics); sources: Widget or Iframe 820, WhatsApp 260, Agent page 160; confidence skewed high, with about 9% of answers below 0.5.
- 2026-11-11 → 2026-11-17 (previous week): conversations 1,148; escalated 149; thumbsUp 205; thumbsDown 41.
- 2026-10-01 → 2026-10-31: conversations 4,960; escalated 710; thumbsUp 860; thumbsDown 190.
Split totals across the 7 buckets plausibly; keep the sums exact.

## Conversations
Ids look like `conv_<word><n>`. Topics in the last 30 days, most to least common: order status (~35%), returns and exchanges (~20%), sizing (~12%), app checkout payment errors (new since Nov 18), shipping countries and costs, warranty, gift cards, store hours.

Key conversations (return them when a search or export matches):
- `conv_brazil1` (2026-11-21, Widget): customer asks "do you ship to São Paulo, Brazil?"; the bot answered "Yes, we ship to Brazil, delivery takes 10-14 days." Wrong (US and Canada only). The answer came from a crawled page https://trailheadsupply.com/blog/patagonia-trip that mentions a Brazilian partner store. Thumbs down.
- `conv_checkout1`, `conv_checkout2`, `conv_checkout3`, `conv_checkout4`, `conv_checkout5`, `conv_checkout6`, `conv_checkout7`, `conv_checkout8`, `conv_checkout9` (2026-11-18 → 2026-11-25): customers on the iOS app (version 5.1) report "Payment failed: error 402" at checkout with Apple Pay; card payment on the website works. The bot suggests clearing the cache and retrying; 6 of them escalated, 4 have thumbs down. Two are in French (Quebec).
- `conv_android1` (2026-11-22): one Android customer says the app "crashed once" when opening a product page; no payment issue. Not the same problem.
- `conv_delivery1`…`conv_delivery5` (this week): late deliveries with carrier "ParcelGo" in Ontario, 3-6 days past the estimate; 2 asked for a refund of shipping.
- `conv_gift1` (2026-11-19): customer asked if gift wrapping is available; bot said "I don't have information on that".
- `conv_unknown1`…`conv_unknown6` (this month): the bot said "I don't have information on that" about: price matching (3 conversations), student discount (2), store pickup in Denver (1).
- `conv_track1`, `conv_track2` (2026-11-10, 2026-11-15): customers asked "can I track my order in the app?"; bot said tracking is only via the email link.
- `conv_return_late1` (2026-11-23): customer delivered 34 days ago wants to return boots; bot explained the 30-day window and created a ticket.
Search for the old return value "30 days" in the last 30 days → about 140 conversations (`total` 140, `hasMore` true).

## Help desk (Trailhead Support)
Statuses: `st_new` New (new), `st_open` Open (on_you), `st_wait` Waiting on customer (on_customer), `st_hold` On hold (on_hold), `st_closed` Closed (closed). Teams: `team_tier1` Tier 1, `team_payments` Payments.
Operators (assignee ids): `usr_maya01` Maya Chen (the user), `usr_ali02` Ali Hassan, `usr_sara03` Sara Lopez.
Open now: 61 owed a reply (`new,on_you`), 14 unassigned, 5 urgent or high, 9 on hold. These counts are exact: filler tickets you invent must fit them (exactly 14 open unassigned tickets, exactly 5 open urgent or high: #1060, #1061, #1051, #1063 and one filler), and every list or total you return must agree with them. Tickets created this week: 172; created 2026-11-25 08:00–16:00 Toronto: 31; closed in that shift: 27. A `chatbase_list_tickets` call with `status: "closed"` sorted by `updatedAt` desc returns those 27 first (updatedAt between 13:00Z and 21:00Z on 2026-11-25), then older closed tickets. Attendance and activity rows cover the whole shift, 08:00–16:00.
Key tickets:
- #1042 "Refund for boots returned last week" (on_you, normal, assigned Ali, customer Jordan Reyes, jordan.reyes@example.com, created 2026-11-20, conversationId conv_refund1): customer returned boots, return received 2026-11-21, asks when the refund arrives. Last message from the customer 2026-11-24.
- #1051, #1055, #1058, #1063 "Payment failed in app" (from conv_checkout1/3/5/8; on_you; two high, two normal; assigned none, Ali, Sara, none; created 2026-11-18 → 2026-11-24). #1063 has an internal note from Sara: "Linked to LIN-482 (iOS Apple Pay 402)". After the user says it's fixed, #1051, #1055, #1058, #1063 are the affected open tickets.
- #1060 "Order 88213 never arrived" (new, urgent, unassigned, created 2026-11-24T21:10Z).
- #1061 "Charged twice" (on_you, high, team Payments, assigned Sara, created 2026-11-25T13:05Z).
- #1012 "Exchange jacket size" (on_customer, low, waiting since 2026-11-09).
- #1019 "Question about warranty" (on_customer, normal, waiting since 2026-11-08).
search_tickets "payment failed" / "402" / "checkout" → #1051, #1055, #1058, #1063. search_tickets "LIN-482" → #1063 only.
Activity today (shift 08:00–16:00 Toronto): Maya worked #1060, #1061, 6 others; Ali worked #1042, #1055, 9 others; Sara worked #1058, #1063, #1061, 7 others. Attendance today: Maya 08:00–16:00, Ali 08:00–16:00 (12 min late), Sara 09:00–17:00.

## Writes
Any create/update/delete call succeeds and returns the written record with new ids (`src_new1`, `proc_new1`, ticket message `msg_new1`…): new sources come back `untrained`. `chatbase_chat` returns a plausible reply from the Trailhead Support bot that follows its current instructions.
