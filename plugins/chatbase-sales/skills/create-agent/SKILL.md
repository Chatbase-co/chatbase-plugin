---
name: create-agent
description: 'Creates a Chatbase agent for a companys website, sales page or landing page, or copies an existing agent for a new product, market or language, then gives it real instructions and a greeting that turn visitors into leads. Use for "make a sales bot for our site", "set up a bot for our new enterprise landing page", "make a Spanish copy of our sales bot", "is my bot ready?". To tune an existing agent for qualifying and booking demos, use sales-agent-setup.'
---

# Create an agent

Never wait for a crawl or for training: start it, finish the setup, and let the user come back.

## From a website

1. Confirm the name and URL. A sitemap URL gives a cleaner crawl than the homepage.
2. Ask in one message, skipping what you already know: what the business sells and to whom, the tone, what the bot must never promise (discounts, custom pricing), and where to send buyers who want a person (a demo link, a sales email or phone). If you can browse, read the homepage instead of asking what the business does.
3. `chatbase_create_agent` with `name` and `url`. This already adds the site as a source and starts the crawl — don't add it again. If `pendingSteps` contains `ADD_SOURCE`, add the site with `chatbase_create_source` (`type: "link"`, `linkType: "sitemap"` or `"crawl"`).
4. The new agent has generic instructions. Draft real ones (role, scope, tone, handoff, never-do rules; about 15 lines), a greeting and three starter questions. Show them; on approval, `chatbase_update_agent` with `instructions`, `initialMessages` and `suggestedMessages`.
5. `chatbase_list_sources` once (the create call returns no source id) and read the site row's `metadata.crawlStatus`. Still fetching: "Your site is being read, usually for a few minutes. Ask me 'is my bot ready?' later." Done: offer three test questions with `chatbase_chat`.
6. Next steps: tune it to qualify visitors and book demos (sales-agent-setup), add pricing and competitor answers (objections), deploy it from the dashboard.

## "Is my bot ready?"

`chatbase_get_agent` (`status`) and `chatbase_list_sources` (the site row's `metadata.crawlStatus` and page counts) together.

## Crawl failed

The site may block crawlers. Add the key pages (pricing, FAQ, contact) as single links with `linkType: "individual"`, and offer to add the key facts (pricing, plans, contact) as text sources with `chatbase_create_source`.

## From an existing agent

1. `chatbase_list_agents`; match the template by name; confirm the new name.
2. `chatbase_clone_agent`. Training starts on its own; don't wait for it. Notion sources aren't copied.
3. Draft the new name, instructions, greeting and starter questions for the new brand or language. Ask for brand facts you don't know (contact details, website). On approval, `chatbase_update_agent` on the copy.
4. Explain that the copied sources still hold the old brand's facts and language. Offer to add the new brand's website (`chatbase_create_source`) and to delete old brand-specific sources (`chatbase_delete_source`, one confirmation each — it can't be undone).

## Ask first

Creating or cloning the agent; the instructions; each source deletion; test chats.

## Watch out

`AGENT_LIMIT_REACHED` means the plan has no free agent slot. Crawl page limits depend on the plan.
