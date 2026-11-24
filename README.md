# AdCopilot for LinkedIn Ads

LinkedIn Ads help in your AI client, through AdCopilot. Today this plugin reads the
LinkedIn ad accounts you connect (campaign groups, campaigns, ads' names, status
and review, conversion rules, the Insight Tag and their results), audits them and
analyses their results, checks your LinkedIn Insight Tag in Google Tag Manager,
reports LinkedIn traffic and key events in Google Analytics (GA4), finds UTM
mistakes, guides conversion setup, plans B2B campaigns, drafts Sponsored Content
copy and does the budget pacing math. It changes nothing in your LinkedIn ad
accounts.

Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with or
endorsed by LinkedIn or Google. LinkedIn is a trademark of LinkedIn Corporation,
and Google Analytics and Google Tag Manager are trademarks of Google LLC. This
plugin is not related to other products named AdCopilot.

The plugin is MIT licensed. The AdCopilot connector it brings is a hosted service, so you need an AdCopilot account to use it.

## What it does today

- **Reads your LinkedIn ad accounts**, through the LinkedIn connector: accounts,
  campaign groups, campaigns, ads' names, status and review, conversion rules, the
  Insight Tag, and LinkedIn's own figures for them, such as spend, clicks and
  leads, with AdCopilot's cost per lead worked out from them.
- **Audits them**: a scored audit, wasted spend, reach, frequency and ad fatigue,
  budget pacing, bidding, campaigns that are not serving, and results by ad. The
  score and its checks are AdCopilot's, not LinkedIn's.
- **Analyses their results**: two periods compared, results over time, results by
  placement, serving location, device or objective, and conversions by conversion
  rule and campaign.
- **Checks your LinkedIn Insight Tag in Google Tag Manager** and stages a tag or a
  thank-you-page trigger for you to publish, only on your yes. The change lands in
  a workspace named AdCopilot in Tag Manager and is never published for you.
- **Reports LinkedIn traffic and key events in Google Analytics (GA4)** by source,
  medium and campaign, finds UTM mistakes and writes a UTM template.
- **Guides conversion setup** in LinkedIn Campaign Manager, from LinkedIn's own
  help pages, stated at the time of writing.
- **Plans B2B campaigns, drafts Sponsored Content copy and does budget pacing and
  cost-per-lead math.** This is Claude's own work, from what you tell it.

It only reads your LinkedIn ad accounts. When a finding calls for a change, such
as pausing a campaign that spends with no result, Claude says what to change and
where in Campaign Manager you make it.

## What it does not read

It never reads your LinkedIn profile, your posts, your Pages, your leads or
audience demographics, and it leaves your campaigns' targeting criteria and your
ads' text and images out.

## Plans

Reading LinkedIn ad accounts is not part of the Free plan. The LinkedIn
connector's own answer says what your workspace's plan includes.

## Install

Two connectors, two sign-ins: `adcopilot`, for Google Tag Manager and Google
Analytics, and `li`, for your LinkedIn ad accounts. Then connect your Google
products and your LinkedIn login once, in AdCopilot at
https://app.adcopilot.cloud, not in your AI client.

### Claude Code

1. Add the repository as a marketplace:
   `/plugin marketplace add AtromxIntelligence/adcopilot-linkedin-ads-plugin`
2. Install the plugin:
   `/plugin install adcopilot-linkedin-ads@adcopilot-linkedin-ads-plugin`
3. Run `/mcp`, sign in to the AdCopilot connector, then to
   `plugin:adcopilot-linkedin-ads:li`.

### Claude on the web and the Claude desktop app

1. Go to **Customize**, then **Plugins**, search for AdCopilot for LinkedIn Ads
   and click **Add**.
2. Open the plugin, open its **Connectors** tab, click **Connect** beside
   `adcopilot` and sign in, then do the same beside `li`.

### Cowork

The same steps as on the web: **Customize**, **Plugins**, add AdCopilot for
LinkedIn Ads, then its **Connectors** tab, **Connect** `adcopilot` and `li`, and
sign in to each.

The plugin registers both connectors for you, so there is no need to add a
connector by hand. Then run the setup command, `/adcopilot-linkedin-ads:setup`, to
see what is connected.

## Already use another AdCopilot plugin?

There is one connector and one AdCopilot account, whichever AdCopilot plugins you add.
Every AdCopilot plugin points at the same address, so your AI client treats them as one connector.
In Claude Code, `/mcp` shows the connector once, under whichever AdCopilot plugin loaded first, and the sign-in belongs to that entry.
If Claude asks you to sign in again after you add or remove an AdCopilot plugin, run `/mcp` and sign in once.
The `li` connector belongs to this plugin and has its own sign-in.

## Data

The plugin is instructions only: it runs no code and sends nothing anywhere itself.
The AdCopilot connector at mcp.adcopilot.cloud reads and, on your yes, writes your Google products through Google's APIs with your Google sign-in.
The LinkedIn connector at mcp.adcopilot.cloud/linkedin/mcp reads your LinkedIn ad accounts through LinkedIn's API with your LinkedIn sign-in, each time you or your AI assistant asks.
On its own, every 6 days, it checks which ad accounts your login still holds a role on.
AdCopilot keeps your LinkedIn sign-in and the ad accounts it reaches, with your role on each, all encrypted, and a 180-day log of which tool ran on which account, with no campaign data.
It does not keep your results.
Disconnecting LinkedIn on your AdCopilot dashboard deletes your LinkedIn sign-in and your roles at once.

LinkedIn results go to the AI assistant you chose, which is made by a separate company: its terms and your settings there decide how long it keeps them and whether it trains on them.
AdCopilot is AI-powered: what your AI assistant says from LinkedIn results is AI-generated and may be wrong, so check it before you act on it. AdCopilot does not train AI models on LinkedIn data. Report a harmful or wrong answer to support@adcopilot.cloud.

The skills end with lists of pages you can open to check an answer: LinkedIn's help pages at www.linkedin.com, and Google's at support.google.com and developers.google.com.
They are links for you to read.
The plugin does not fetch them and sends nothing to them.

Privacy policy: https://adcopilot.cloud/privacy.
Terms: https://adcopilot.cloud/terms.
Documentation: https://adcopilot.cloud/docs/.

## What you get

Commands, which Claude Code namespaces by plugin name:

- `/adcopilot-linkedin-ads:setup` checks both sign-ins and says what is connected.
- `/adcopilot-linkedin-ads:review` reviews your LinkedIn ad accounts.
- `/adcopilot-linkedin-ads:check` checks the Insight Tag in Tag Manager.
- `/adcopilot-linkedin-ads:plan` plans a campaign and drafts Sponsored Content.

Skills, which Claude loads by what you ask:

- `linkedin-connect` connects your LinkedIn login and passes on the connector's own
  words.
- `linkedin-review` reads accounts, campaigns, ads and the Insight Tag checks.
- `linkedin-audit` runs the audit and its checks.
- `linkedin-analysis` compares periods and shows trends, breakdowns and
  conversions.
- `linkedin-ads-tracking` checks the Insight Tag in Tag Manager and stages a tag or
  trigger.
- `linkedin-ads-traffic` reports LinkedIn traffic in Google Analytics and writes
  UTM templates.
- `linkedin-ads-plan` plans a B2B campaign and drafts copy.
- `linkedin-ads-budget` does the pacing and cost-per-lead sums from your figures.

Every skill says what it cannot see, and LinkedIn figures are reported on their
own, never added to or compared with Google figures in one table or total.

## Example prompts

After you sign in, ask in your own words. For example:

- "How are my LinkedIn campaigns doing, and what does a lead cost me?"
- "Audit my LinkedIn ad account and show me where the money is wasted."
- "Why is my LinkedIn campaign not serving?"
- "Is my LinkedIn Insight Tag set up in Google Tag Manager?"
- "How much traffic does LinkedIn send to my site in Google Analytics, and are my UTM tags right?"
- "Plan a B2B campaign for our new product and draft the Sponsored Content copy."

## What it will not do

- Change, pause, switch on or delete anything in your LinkedIn ad accounts.
- Publish or delete anything in Tag Manager, or delete anything in Analytics.
  Tag Manager changes are staged for you to publish.
- Change anything without your yes, to that change, in that conversation.
- Send a LinkedIn result to another tool, such as a spreadsheet export.
- Invent a number. The numbers are the tool's, or yours, or worked out from yours.

## Support

Open an issue at https://github.com/AtromxIntelligence/adcopilot-linkedin-ads-plugin/issues
or write to support@adcopilot.cloud.

To report a security problem, write to support@adcopilot.cloud.

## Version

**0.2.0 (2026-11-25, written against AdCopilot v2.46.45, live since 2026-11-25)**
The LinkedIn connector, `li`, beside `adcopilot`: this plugin now reads, audits
and analyses the LinkedIn ad accounts you connect, read only. Four new skills
(connect, review, audit and analysis) and a review command. The older four skills
point to them for LinkedIn's own figures, and the setup command covers both
sign-ins.

**0.1.2 (2026-11-05)**
Changes nothing you use. The plugin folder now holds only the files Claude loads,
and this page says where to report a security problem.

**0.1.1 (2026-10-25, written against AdCopilot v2.44.0, live since 2026-10-22)**
Text only. Every place that said what comes later said that direct access to your
LinkedIn ad account was being built, with no date.

**0.1.0 (2026-10-23, written against AdCopilot v2.44.0, live since 2026-10-22)**
First release. Four skills and three commands: the LinkedIn Insight Tag check and
staging in Google Tag Manager, LinkedIn traffic and key events in Google Analytics
(GA4) with UTM hygiene, B2B campaign plans and Sponsored Content drafts, and
budget pacing math.

## Licence

MIT, copyright 2026 Atromx Intelligence Private Limited. See the LICENSE file.
