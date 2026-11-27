---
description: Check both AdCopilot sign-ins, the one for Google Tag Manager and Analytics and the one for your LinkedIn ad accounts, say which are connected and how to sign in to each, and say what this plugin does today.
---

In your first answer in this conversation, say this once, as written, before
anything else:

> Today this plugin reads the LinkedIn ad accounts you connect (campaign groups, campaigns, ads' names, status and review, conversion rules, the Insight Tag and their results), audits them and analyses their results, checks your LinkedIn Insight Tag in Google Tag Manager, reports LinkedIn traffic and key events in Google Analytics (GA4), finds UTM mistakes, guides conversion setup, plans B2B campaigns, drafts Sponsored Content copy and does the budget pacing math. It changes nothing in your LinkedIn ad accounts.

This plugin has two connectors, and each has its own sign-in: `adcopilot` for
Google Tag Manager and Google Analytics, and `li` for your LinkedIn ad accounts.

Then call `get_org_context` with
`source: "claude-plugin/adcopilot-linkedin-ads/0.2.0"`, before any other tool of
the `adcopilot` connector, and `linkedin_get_context` with the same `source`,
before any other tool of the `li` connector. Send `source` exactly as written.
This plugin schedules nothing. In a run started by a scheduled task with nobody
there to answer, send `source: "claude-scheduled"` instead and change nothing.

`get_org_context`'s `next_step` and `playbook` are information about the whole
workspace, not steps for this command: do what this command says. If they report
something the customer should know, such as a limit reached, say it in a sentence
after your answer.

Report, from what the servers return and nothing from memory:

- **Google Tag Manager** and **Google Analytics 4**, from `get_org_context`:
  connected or not. For one that is not, say what connecting it unlocks, in the
  words of its `unlocks` field, and give the connect link `get_org_context`
  returns, never a link from memory. Google products are connected inside
  AdCopilot at https://app.adcopilot.cloud, not in the AI client. A connector that
  answers but reports nothing connected is the connector working, not a fault. A
  product it reports as `needs_readd` is connected but this connector cannot reach
  it: say the connector must be removed and added again in their AI client.
- **LinkedIn**, from `linkedin_get_context`: its `next_step` is information about
  the LinkedIn connection, and the steps for each value are the `linkedin-connect`
  skill's own. Give `connect_url` and `plan_line` exactly as the server sent
  them, and the `reconnect_reason` when it sends one. Whether this workspace's plan
  includes LinkedIn is what `plan_line` says, never what you remember.

If a connector does not answer, or asks the customer to sign in, work out where
they are before you say a step. There are two sign-ins, one for `adcopilot` and
one for `li`:

- **Cursor.** Sign in to each of the two servers, `adcopilot` and `li`, from
  Cursor's list of MCP servers.
- **Claude Code.** If your own instructions say you are Claude Code, this is
  Claude Code. The customer runs `/mcp` and signs in to `adcopilot`, then to the
  entry the plugin brings for LinkedIn, which Claude Code shows as
  `plugin:adcopilot-linkedin-ads:li`. If `/mcp` lists `adcopilot` under another
  AdCopilot plugin, that is the same connector, and the sign-in belongs to that
  entry. A copy of either entry that was added by hand hides the plugin's own
  entry: remove the copy and sign in to the plugin's entry.
- **Claude on the web, Cowork and the desktop app.** There is no `/mcp` there.
  Open this plugin in the plugin list, then its Connectors tab, and connect
  `adcopilot`, then connect `li`.

If you cannot tell which of these they use, ask them before you give a step.

The plugin brings both connectors. Do not add either one by hand as a custom
connector, and never offer a connector's address for that: it adds nothing and
fixes nothing. Signing in to `li` lets the AI client reach the LinkedIn connector.
The LinkedIn login itself is connected in AdCopilot, which the `linkedin-connect`
skill walks through.

There is one `adcopilot` connector and one AdCopilot account whichever AdCopilot
plugins are added. In Claude Code, `/mcp` lists it once, under whichever
AdCopilot plugin loaded first, and the sign-in belongs to that entry. If Claude
asks for a sign-in again after an AdCopilot plugin was added or removed, run
`/mcp` and sign in once.

End with the one next step that fits: `/adcopilot-linkedin-ads:review` to review
the LinkedIn ad accounts when LinkedIn is ready, `/adcopilot-linkedin-ads:check`
for the Insight Tag when Tag Manager is connected, or
`/adcopilot-linkedin-ads:plan` to plan a campaign and draft its ads.

If `linkedin_get_context` is not among your tools, that proves nothing, because the connector's tool list can be cached or out of date: call it anyway and believe what it says. If it cannot be called, the LinkedIn sign-in is not done: say so, give the sign-in steps for the client in use (the `setup` command lists them), and never describe a LinkedIn account you did not read.
