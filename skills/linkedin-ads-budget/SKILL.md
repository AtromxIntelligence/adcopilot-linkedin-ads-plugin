---
name: linkedin-ads-budget
description: Work out LinkedIn ad budget pacing and cost-per-lead arithmetic from figures the customer gives, with Claude's own math, covering projected spend, the daily amount that lands on budget, over or under pace, and leads needed or affordable at a target cost. AdCopilot reads no LinkedIn data for this. Use when the user asks whether a LinkedIn campaign is on pace, how much to spend per day, how many leads a LinkedIn budget buys, or what a LinkedIn lead costs.
---

# LinkedIn budget pacing

The customer wants arithmetic on a LinkedIn budget. This is your own math, from
figures they give you. AdCopilot reads no LinkedIn data for it and calls no tool,
and you say so once: every number here is theirs or is worked out from theirs,
and LinkedIn's own reports in Campaign Manager, not this arithmetic, are the
figure of record.

## First answer

In your first answer in this conversation, say this once, as written, before
anything else:

> Today it checks your LinkedIn Insight Tag in Google Tag Manager, reports LinkedIn traffic and key events in Google Analytics (GA4) by source, medium and campaign, finds UTM mistakes, guides conversion setup, plans B2B campaigns, drafts Sponsored Content copy and does the budget pacing math. It cannot read your LinkedIn ad account yet. Direct access to your LinkedIn ad account is being built; there is no date.

Do not repeat it in later answers unless they ask what this plugin can do.

## What to ask for

Ask for only what the sum needs, one question at a time, and use their words and
their currency. Do not convert a currency. Never fill a gap with a typical figure
or a benchmark.

- For pacing: the budget for the period, the first and last day of the period,
  today's date, and the spend so far from their Campaign Manager.
- For cost per lead: the spend and the number of leads over the same dates, and
  for planning, a target cost per lead or a target number of leads.

## The sums

Show each formula once, then the working with their numbers, then the answer in
a sentence. Say what each figure is: theirs, or worked out.

- **Spend per day so far** is the spend so far divided by the days that have
  passed, counting today only if the spend so far includes today.
- **Projected spend** is that daily figure times the days in the period.
- **Pace** is the projected spend divided by the budget. Call it on pace when it
  is within about 10 percent either way, over when it is above that and under
  when it is below, and say that the 10 percent is this skill's rule of thumb and
  not LinkedIn's.
- **The daily amount that lands on budget** is the budget left (the budget minus
  the spend so far) divided by the days left. If nothing is left, or the spend is
  already past the budget, say so and give no daily amount.
- **Cost per lead** is the spend divided by the leads. With no leads, there is no
  cost per lead: say that, and do not divide by zero or write infinity.
- **Leads the budget buys** is the budget divided by the cost per lead, at the
  cost per lead they gave, and **the budget a lead target needs** is the target
  times that cost.

Check the inputs before you work on them. If the period has not started, or no
day has passed, there is nothing to project: say so. If the dates, the budget or
the spend do not make sense together, ask, and do not guess which is wrong.

State the assumption behind every projection: it holds the daily pace so far
flat. A campaign's delivery can vary from day to day, and a change to the budget, the
audience or the ads moves it. A cost per
lead from a handful of leads is a weak figure, and you say how many leads it
rests on.

## Changes

This skill changes nothing and calls no tool. Every change is proposed first,
with what it changes and how to undo it, and is applied only after the customer's
explicit yes in this conversation. A yes to one change is not a yes to another.
Nothing is ever deleted. If the sums say the daily budget should move, say what
to change and that they make it in Campaign Manager themselves.

## What this cannot see

Their LinkedIn ad account: the real spend, the real leads and the delivery since
the figures were copied. A figure they typed in is theirs, and you label it that
way. Say which of these mattered to the answer.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a
sentence: a campaign plan for the budget, or how LinkedIn visits look in Google
Analytics.
