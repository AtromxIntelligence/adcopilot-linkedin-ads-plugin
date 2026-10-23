# AdCopilot for LinkedIn Ads

LinkedIn Ads help in your AI client, through AdCopilot. Today it works from your
own Google Tag Manager and Google Analytics (GA4), and from the figures you give
it:

- **Checks your LinkedIn Insight Tag in Google Tag Manager.** It reads the
  container's tags and triggers (`gtm_list_accounts`, `gtm_list_containers`,
  `gtm_list_workspaces`, `gtm_list_tags`, `gtm_list_triggers`,
  `gtm_list_version_headers`) and tells you what is there: no LinkedIn tag, two
  site-wide tags, a paused tag, a tag with no trigger or a narrow one.
- **Stages a tag or a thank-you-page trigger for you to publish** (`gtm_create_trigger`,
  `gtm_create_tag`), only on your yes. The change lands in a workspace named
  AdCopilot in Tag Manager and is never published.
- **Reports LinkedIn traffic and key events in Google Analytics (GA4)** by source,
  medium and campaign (`ga4_list_account_summaries`, `ga4_get_metadata`,
  `ga4_run_report`, `ga4_list_conversion_events`), finds UTM mistakes that split
  or hide LinkedIn traffic, and writes a UTM template for each campaign.
- **Guides conversion setup** in LinkedIn Campaign Manager, from LinkedIn's own
  help pages, stated at the time of writing (checked 23 October 2026).
- **Plans B2B campaigns, drafts Sponsored Content copy, and does budget pacing and
  cost-per-lead math.** This is Claude's own work, from what you tell it.
  AdCopilot reads no LinkedIn data for it.

**What comes later.** AdCopilot cannot read your LinkedIn ad account yet. Direct
access is planned for when LinkedIn approves AdCopilot's API access, and there is
no date.

Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with or
endorsed by LinkedIn. LinkedIn, Insight Tag and Sponsored Content are trademarks
of LinkedIn Corporation or their respective owners. This plugin is not related to
other products named AdCopilot.

The plugin is free (MIT). The AdCopilot connector is a hosted service: Free plan available; paid plans on https://adcopilot.cloud/pricing

## Install

Two steps on every surface: add the plugin, then sign in to the connector it
brings with it. Then connect your Google products once, in AdCopilot at
https://app.adcopilot.cloud, not in your AI client.

### Claude Code

1. Add the repository as a marketplace:
   `/plugin marketplace add AtromxIntelligence/adcopilot-linkedin-ads-plugin`
2. Install the plugin:
   `/plugin install adcopilot-linkedin-ads@adcopilot-linkedin-ads-plugin`
3. Run `/mcp`, choose the AdCopilot connector and sign in.

### Claude on the web and the Claude desktop app

1. Go to **Customize**, then **Plugins**, search for AdCopilot for LinkedIn Ads
   and click **Add**.
2. Open the plugin, open its **Connectors** tab, click **Connect** beside
   `adcopilot`, and sign in.

### Cowork

The same two steps as on the web: **Customize**, **Plugins**, add AdCopilot for
LinkedIn Ads, then its **Connectors** tab, **Connect** `adcopilot`, and sign in.

The plugin registers the connector for you, so there is no need to add a custom
connector by hand. Then run the setup command, `/adcopilot-linkedin-ads:setup`,
to see what is connected.

## Already use another AdCopilot plugin?

It is one connector and one sign-in, whichever AdCopilot plugins you add. Every
AdCopilot plugin points at the same address, `https://mcp.adcopilot.cloud/mcp`.
In Claude Code, `/mcp` shows the connector once, under whichever AdCopilot plugin
loaded first. In Claude on the web, the desktop app and Cowork, Claude links a
connector by its address, so these plugins use the one connector on your account;
if this plugin's Connectors tab shows `adcopilot` as not connected, connect it
there once. If Claude asks you to sign in again after you remove an AdCopilot
plugin, run `/mcp` and sign in once.

## What you get

Commands, which Claude Code namespaces by plugin name:

- `/adcopilot-linkedin-ads:setup` checks the connector and says what is connected.
- `/adcopilot-linkedin-ads:check` checks the Insight Tag in Tag Manager.
- `/adcopilot-linkedin-ads:plan` plans a campaign and drafts Sponsored Content.

Skills, which Claude loads by what you ask:

- `linkedin-ads-tracking` checks the Insight Tag and stages a tag or trigger. It
  uses `get_org_context` and the Tag Manager tools named above.
- `linkedin-ads-traffic` reports LinkedIn traffic and key events and writes UTM
  templates. It uses `get_org_context` and the Analytics tools named above.
- `linkedin-ads-plan` plans a B2B campaign and drafts copy. It reads only the
  saved business profile, through `get_org_context`.
- `linkedin-ads-budget` does the pacing and cost-per-lead sums from your figures.
  It uses no tool.

Every skill says what it cannot see, and writes LinkedIn's screens and limits as
"at the time of writing", with the date they were checked.

## What it will not do

- Read your LinkedIn ad account. It has no access to it today.
- Publish anything in Tag Manager. Changes are staged for you to publish.
- Delete anything.
- Change anything without your yes, to that change, in that conversation.
- Invent a number. The numbers are the tool's, or yours, or worked out from yours.

## Data

The plugin is instructions only: it runs no code and sends nothing anywhere
itself. The AdCopilot connector at mcp.adcopilot.cloud reads and, on your yes,
writes your Google products through Google's APIs with your Google sign-in. The
skills name a few LinkedIn and Google help pages for you to read; the plugin
fetches none of them. Privacy policy: https://adcopilot.cloud/privacy. Terms:
https://adcopilot.cloud/terms. Documentation: https://adcopilot.cloud/docs/.

## Support

Open an issue at https://github.com/AtromxIntelligence/adcopilot-linkedin-ads-plugin/issues
or write to support@adcopilot.cloud.

## Version

**0.1.0 (2026-10-23, written against AdCopilot v2.44.0, live since 2026-10-22)**
First release. Four skills and three commands: the LinkedIn Insight Tag check and
staging in Google Tag Manager, LinkedIn traffic and key events in Google Analytics
(GA4) with UTM hygiene, B2B campaign plans and Sponsored Content drafts, and
budget pacing math. Reading a LinkedIn ad account is not part of this version.

## Licence

MIT, copyright 2026 Atromx Intelligence Private Limited. See the LICENSE file.

## What CI runs

On every push to main and every pull request, GitHub Actions runs two jobs. The
first, structural, installs a pinned Claude Code, runs the plugin validator in its
strict mode on the plugin and on its manifest, checks that the manifests parse,
that every skill and command has a name and a description, that no
download-and-execute pattern is present and that the manifest version is not
behind the latest tag, and runs the stdlib unit tests in the tests folder. They
check the manifest fields, the file sizes, that every tool a skill names is one
the connector serves, and that nothing reads a credential. The second job,
gitleaks, scans every commit for secrets. Neither job needs a secret of its own.
