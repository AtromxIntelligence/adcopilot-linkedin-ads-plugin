---
description: Review your connected LinkedIn ad accounts with LinkedIn's own figures, cost per lead, conversions and the Insight Tag checks, read only, then offer an audit or a deeper analysis.
---

Follow the `linkedin-review` skill.

If the customer typed something after the command, use it to choose the ad
account, the campaign or the dates, and do not ask for it again: $ARGUMENTS

Offer the `linkedin-audit` skill when the customer wants a scored audit, and the
`linkedin-ads-traffic` skill when they want LinkedIn traffic in Google Analytics
(GA4), as a separate report never compared with LinkedIn's figures.

If `linkedin_get_context` is not among your tools, that proves nothing, because the connector's tool list can be cached or out of date: call it anyway and believe what it says. If it cannot be called, the LinkedIn sign-in is not done: say so, give the sign-in steps for the client in use (the `setup` command lists them), and never describe a LinkedIn account you did not read.
