# Launch readiness

What a new project needs before its first customer, beyond the code. `chart` turns each item
into a decision ticket, `spec` records the outcome in its Launch section, `slice` turns the
work into `astack:launch` slices, and `ship` checks they are closed before the first
customer-facing release.

An item that doesn't apply (for example payments on a free product) is ruled out of scope on
the map, with the reason, instead of being skipped silently.

| Item | The decision |
|---|---|
| **First customer** | Who they are, how they get access (invite, sign-up, waitlist), and what they must be able to do on day one |
| **Domain and email** | The domain, DNS host, and production URL; the sending domain for transactional email, with SPF, DKIM, and DMARC |
| **Payments** | Whether to charge at launch; provider, pricing, trial, and the live-mode switch (live keys only in `production`, webhooks per environment) |
| **Legal** | Terms of service and privacy policy; cookie consent and data-export or deletion requests for the regions served |
| **Accounts and data** | Account deletion, production backups with a tested restore, and data retention |
| **Measurement** | The one event that shows a customer got value, and the analytics that record it in production only |
| **Operations** | Who is alerted when production errors or goes down, through which channel, plus uptime monitoring on the health endpoint |
| **Support and feedback** | How customers reach you, and how their reports become GitHub issues (`astack:bug`, or a request routed through `astack`) |

## Ticket types

- Choosing a provider or tool (payments, email, analytics, monitoring) is a `decision:research`
  ticket for the scout, followed by a `decision:grilling` ticket only if the findings leave a
  real choice.
- Who the first customer is, pricing, and anything legal are `decision:grilling`: those are the
  user's calls.
- Signing up for a service so its terms or API can be judged is a `decision:task`.

## Work after the decisions

The spec's Launch section splits each decided item into:
- **Build work** (legal pages, deletion endpoint, analytics event, health monitoring): normal
  slices labelled `astack:launch`.
- **User work** (buying the domain, activating live payments, signing provider terms): slices
  labelled `astack:launch` and `astack:release`, assigned to the user, with a checklist body.
  Agents never take them because they are already assigned, and development runs don't wait
  on them.
