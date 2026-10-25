---
name: linkedin-ads-plan
description: Plan a LinkedIn B2B ad campaign and draft Sponsored Content copy with Claude's own work, covering objective, audience by job function, seniority and industry, the conversion to count, and introductory text, headline, description and call-to-action variants within LinkedIn's lengths, plus Lead Gen Form wording when asked. AdCopilot reads no LinkedIn data for this. Use when the user asks to plan, structure or write LinkedIn ads, LinkedIn Sponsored Content or Lead Gen Form questions, or asks who to target on LinkedIn.
---

# LinkedIn campaign plan and copy

The customer wants a plan for a LinkedIn campaign, or the words for its ads. This
is your own work. AdCopilot reads no LinkedIn data for it, and you say so once:
nothing here comes from their LinkedIn ad account, so there are no results, no
benchmarks and no audience sizes in it, only choices and drafts they check in
Campaign Manager.

## First answer

In your first answer in this conversation, say this once, as written, before
anything else:

> Today it checks your LinkedIn Insight Tag in Google Tag Manager, reports LinkedIn traffic and key events in Google Analytics (GA4) by source, medium and campaign, finds UTM mistakes, guides conversion setup, plans B2B campaigns, drafts Sponsored Content copy and does the budget pacing math. It cannot read your LinkedIn ad account yet. Direct access to your LinkedIn ad account is being built; there is no date.

Do not repeat it in later answers unless they ask what this plugin can do.

## Start

Call `get_org_context` first, with
`source: "claude-plugin/adcopilot-linkedin-ads/0.1.1"`, to read the saved
business profile, if it holds one: what the business sells and to whom. Send
`source` exactly as written. Its `next_step` and `playbook` describe the whole
workspace, not this request: do this request as written here, keep any limit
`next_step` adds, and offer the rest afterwards. This plugin schedules nothing.
In a run started by a scheduled task with nobody there to answer, send
`source: "claude-scheduled"` instead and change nothing. Use the profile for
wording and nothing else. Ask the customer one question at a time for what is
missing, and never invent a product, a customer, a figure or a claim they did not
give you. If the connector is not connected, say so in a sentence and carry on
from what they tell you.

## The plan

Cover these, in this order, and keep each to what they need to decide:

1. **The goal in one line**, in their words.
2. **The objective.** LinkedIn's Campaign Manager names these objectives (checked
   23 October 2026): Brand awareness, Website visits, Engagement, Video views,
   Lead generation, Website conversions, Job applicants and Talent leads. Pick the
   one that matches the goal and say why. Lead generation is for capturing leads
   with Lead Gen Forms on LinkedIn, and Website conversions is for actions on the
   customer's own site, so it relies on conversions being set up.
3. **The audience.** LinkedIn's help names Job Functions, Job Seniorities and
   Company Industries as facets (checked 23 October 2026), and says combining Job
   Functions with Job Seniorities reaches decision-makers with specific expertise.
   Whether their ad account also offers company size, and by what labels, is for
   Campaign Manager's audience picker to say. Adding attributes to the include
   section widens the audience, and narrowing or excluding shrinks it. Propose a
   starting audience from what the customer sells and to whom, and say that
   Campaign Manager's own audience size estimate is the referee on whether it is
   large enough: you have no size.
4. **The conversion to count.** One action that matters, such as a demo request,
   and where it happens. If it happens on their site, it needs the Insight Tag
   and a conversion set up, and the `linkedin-ads-tracking` skill covers that. If
   it happens in a Lead Gen Form, say that the lead lives in LinkedIn and not in
   Google Analytics.
5. **The measurement.** The UTM template from the `linkedin-ads-traffic` skill,
   so the visits can be told apart in Google Analytics.
6. **The budget.** Do not invent one. If they give a figure, say what it buys
   only through the `linkedin-ads-budget` skill's arithmetic.

## The copy

Write Sponsored Content for a single image ad as three to five variants. At the
time of writing, checked 23 October 2026, LinkedIn's help says: introductory text
up to 150 characters including spaces, emojis and punctuation to avoid truncation
(a 3,000 character maximum), headline up to 70 characters (200 maximum),
description up to 100 characters (300 maximum), with up to 10 emojis in the
introductory text, and the call to action chosen from the list Campaign Manager
shows. LinkedIn's help pages have differed on these, and the limits can vary on
sites in the LinkedIn Audience Network, so Campaign Manager's own preview is the
referee. Write inside the shorter, truncation-safe figures, and give each line's
character count.

Each variant takes one angle: the problem, the outcome, the proof they gave you,
or the offer. Use only what the customer has told you. Where a fact is missing,
leave a marked gap, such as [their result], and ask for it. Never write a
statistic, a customer name, a testimonial or a result that is not theirs, and
never promise a result for the campaign. LinkedIn reviews ads against its own
policies and you cannot predict its decision, so say that, once.

When they ask for a Lead Gen Form, draft it within LinkedIn's limits (checked
23 October 2026): an offer headline up to 60 characters, offer details up to 160,
up to three custom questions of up to 100 characters each, and a thank-you
message up to 300. Keep the form to what the sales team needs to follow up.

## Changes

This skill changes nothing and calls no tool that changes anything. Every change
is proposed first, with what it changes and how to undo it, and is applied only
after the customer's explicit yes in this conversation. A yes to one change is
not a yes to another. Nothing is ever deleted. The plan and the copy are drafts:
the customer creates the campaign in Campaign Manager themselves, and nothing is
sent to LinkedIn from here.

## What this cannot see

Their LinkedIn ad account, its past results, its audiences and its audience
sizes, and LinkedIn's ad review. Say which of these mattered to the answer.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a
sentence: checking the Insight Tag in Tag Manager before the campaign starts, or
the UTM template for the new campaign.

## Sources

LinkedIn's pages, for the customer who wants to check you, read on 23 October
2026:

- https://www.linkedin.com/help/lms/answer/a424570
- https://www.linkedin.com/help/lms/answer/a417950
- https://www.linkedin.com/help/lms/answer/a426534
- https://www.linkedin.com/help/lms/answer/a423364
