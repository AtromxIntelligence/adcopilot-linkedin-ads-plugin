---
name: setup
description: Check the AdCopilot connector is connected and signed in, and say which Google products it can reach for LinkedIn Ads work.
---

In your first answer in this conversation, say this once, as written, before
anything else:

> Today it checks your LinkedIn Insight Tag in Google Tag Manager, reports LinkedIn traffic and key events in Google Analytics (GA4) by source, medium and campaign, finds UTM mistakes, guides conversion setup, plans B2B campaigns, drafts Sponsored Content copy and does the budget pacing math. It cannot read your LinkedIn ad account yet. Direct access to your LinkedIn ad account is being built; there is no date.

Then call `get_org_context` with
`source: "claude-plugin/adcopilot-linkedin-ads/0.1.1"`. Send `source` exactly as
written. This plugin schedules nothing. In a run started by a scheduled task with
nobody there to answer, send `source: "claude-scheduled"` instead and change
nothing.

Say plainly which of the two products this plugin works from are connected:
Google Tag Manager, for the Insight Tag check, and Google Analytics 4, for
LinkedIn traffic. For each one that is not, say what connecting it unlocks, in the
words of its `unlocks` field, and give the connect link `get_org_context`
returns, never a link from memory. Google products are connected inside AdCopilot
at https://app.adcopilot.cloud, not in the AI client. A connector that answers
but reports nothing connected is the connector working, not a fault: send them
there instead of letting them hunt for a broken connector. A product it reports
as `needs_readd` is connected but this connector cannot reach it: say the
connector must be removed and added again in their AI client. A tool that is
missing from your list proves nothing, because the list can be out of date: go by
what `get_org_context` says.

If the connector does not answer, or asks the customer to sign in, work out where
they are before you say a step:

- **Claude Code.** If you can run `claude mcp list`, this is Claude Code. The
  customer opens `/mcp`, chooses the AdCopilot connector and signs in. `/mcp`
  lists it once, under whichever AdCopilot plugin loaded first, however many
  AdCopilot plugins they have.
- **Claude on the web, the desktop app and Cowork.** There is no `/mcp` there.
  They open this plugin in the plugin list, then its Connectors tab, and Connect
  `adcopilot`. Never offer "Add custom connector" or the connector's address to
  someone who has this plugin installed in Claude: the plugin already brings the
  connector, so that adds nothing and fixes nothing.

There is one connector and one AdCopilot account whichever AdCopilot plugins are
added. In Claude Code, `/mcp` lists it once, under whichever AdCopilot plugin
loaded first, and the sign-in belongs to that entry. If Claude asks for a
sign-in again after an AdCopilot plugin was added or removed, run `/mcp` and
sign in once.

End with the one next step that fits what is connected: `/adcopilot-linkedin-ads:check`
for the Insight Tag when Tag Manager is connected, or a question about how
LinkedIn traffic looks in Google Analytics when Analytics is. Offer a plan with
`/adcopilot-linkedin-ads:plan` when neither is connected.
