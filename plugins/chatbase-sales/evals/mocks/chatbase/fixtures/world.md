# The account: Orbitly (fictional test company)

Today is Wednesday 2026-11-25, 15:00 America/Toronto. Orbitly sells field-service scheduling software (job scheduling, dispatch, invoicing) to plumbing, HVAC, electrical and landscaping companies in the US and Canada. Plans: Starter $49/month (up to 5 technicians), Growth $199/month (up to 25 technicians), Enterprise custom pricing (25+ technicians, SSO, API, dedicated onboarding). Annual billing gives 2 months free. There are no other discounts. Integrations: QuickBooks Online, Xero, Stripe, Google Calendar; a public API on Enterprise only. The main competitor visitors mention is "CrewPilot" (fictional), which advertises $29/month.

## whoami
userId `usr_sam01`, teamName "Orbitly", plan "Standard", all read and write scopes, plus `leads:read`.

## Agents (chatbase_list_agents)
1. id `agt_orbit_sales`, name "Orbitly Website Assistant", status `trained`, model `gpt-5.5`, lastMessageAt 2026-11-25T19:10:00Z, creditLimit 10000, creditsUsed 4120.
Only this agent exists. Any other agentId → error `AGENT_NOT_FOUND`.

## Settings (chatbase_get_agent)
- instructions: "You are Orbitly's website assistant. Help visitors understand Orbitly and choose a plan. Be concise and friendly.\n- Plans: Starter $49/month (up to 5 technicians), Growth $199/month (up to 25), Enterprise custom pricing.\n- If a visitor wants a demo, use book_demo.\n- If you don't know, say \"I don't have information on that\" and offer the lead form.\n- Never promise features that aren't listed on orbitly.example."
- initialMessages: ["Hi! I'm Orbitly's assistant. Want to see how Orbitly schedules your crew?"]; suggestedMessages: ["See pricing", "How does dispatch work?"].
- channels: website widget and the agent page.

## Sources
`src_site` crawl https://orbitly.example (86 pages, trained); `src_pricing` text "Pricing and plans" (trained); `src_integrations` qna "FAQ: integrations" (trained). No source about competitors or security. Source text can't be read.

## Actions
- `act_leads` name `collect_leads`, type `collect-leads`, enabled, fields name, email, company, number of technicians; whenToUse "When the visitor asks to be contacted."
- `act_demo` name `book_demo`, type `calendly-get-slots`, enabled, whenToUse "When the visitor asks for a demo."
- `act_live` name `live_chat`, type `chatbase-live-chat`, enabled.
No procedures exist (`chatbase_list_procedures` returns an empty list).

## Analytics
- 2026-11-18 → 2026-11-24 (this week): conversations 412; actionTypes collect-leads 38, calendly-get-slots 21; escalated 9; thumbsDown 14; sources: Widget or Iframe 351, Agent page 61.
- 2026-11-11 → 2026-11-17 (previous): conversations 389; collect-leads 29; calendly-get-slots 15; escalated 7; thumbsDown 9.

## Collected data (chatbase_list_collected_data, action collect_leads), newest first
Submissions since 2026-11-24 00:00 Toronto ("today's leads" = these five plus lead_06):
- `lead_01` 2026-11-25 14:20: name Priya Nair, email priya.nair@acmeplumbing.example, company Acme Plumbing, technicians 45. conversation `conv_l01`: asked about Enterprise pricing for 45 technicians, SSO with Google Workspace, migrating job history from CrewPilot; "we want to switch before our CrewPilot renewal on Jan 15"; was shown demo slots and chose none yet.
- `lead_02` 2026-11-25 11:05: name Tom B, email tomslawn@gmail.example, company Tom's Lawn Care, technicians 2. `conv_l02`: asked the price of Starter and whether there's a free plan.
- `lead_03` 2026-11-25 09:40: name Marcus Lee, email marcus.lee@northgateelectric.example, company Northgate Electric, technicians 120. `conv_l03`: asked whether the API can push jobs from their ERP, about QuickBooks Online sync for invoices, said "we're evaluating three vendors and deciding by December 15". The bot said the API is on Enterprise.
- `lead_04` 2026-11-24 16:30: name Dana Kim, email dana@brightpathhvac.example, company BrightPath HVAC, technicians 18. `conv_l04`: asked the price of Growth for 18 technicians and whether annual billing is cheaper; the bot answered "Yes, annual billing saves 20%". (Wrong: it is 2 months free, about 17%.)
- `lead_05` 2026-11-24 13:15: name J Ortiz, email j.ortiz@outlook.example, company (empty), technicians (empty). `conv_l05`: an existing customer asking how to reset their password. Not a sales lead.
- `lead_06` 2026-11-24 10:02: name Lena Fischer, email lena@greenroots.example, company GreenRoots Landscaping, technicians 9. `conv_l06`: asked how dispatch works on mobile and whether Growth includes route planning.
Older this week (2026-11-18 → 2026-11-23): 32 more submissions (filler, plausible small companies) for 38 in the week. Previous week: 29.

## Other conversations (this week)
- Enterprise pricing without leaving details: `conv_e1` (150 technicians, "need SOC 2 report"), `conv_e2` (200 technicians, "price per tech for enterprise?"), `conv_e3` (60 technicians, asked about SSO): each asked about Enterprise pricing; the bot said "Enterprise is custom pricing" and ended without offering the lead form or demo; none left details.
- Competitor: `conv_c1`…`conv_c4` compare Orbitly with CrewPilot; in `conv_c1`, `conv_c2` the bot said "I don't have information on that"; `conv_c3`: "CrewPilot is $29, why are you $49?", the bot repeated the Starter price with no reason; `conv_c4`: asked whether job history can be imported from CrewPilot, the bot said "I don't have information on that".
- `conv_disc1` (2026-11-20): visitor asked for a discount for 3 years upfront; the bot said "We can offer 25% off for a 3-year commitment". (Wrong: no such discount.) The visitor left email ben@ridgewayplumbing.example via the lead form on 2026-11-20.
- Pricing questions this month: about 60 conversations mention "pricing" (`hasMore` true); most ask Starter vs Growth, per-technician cost, annual billing.

## Writes
Any create or update succeeds and returns the written record; new procedures come back `disabled`. `chatbase_chat` returns a plausible reply from the Orbitly assistant following its current instructions.
