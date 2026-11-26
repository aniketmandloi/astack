---
name: chart
description: Plan a large or foggy effort - a brand-new project, a major feature, a rewrite or migration - that is too big for one agent session, as a map of decision tickets on GitHub, then resolve one ticket per session until the way is clear and a spec can be written. Use with a loose idea to chart a new map, or with a map issue to work its next ticket.
argument-hint: "[idea | map issue]"
---

# Chart

A loose idea has arrived, too big for one session and wrapped in fog. Charting finds the way to
the **destination** rather than charging at it. The map lives on GitHub as one issue labelled
`astack:map`; its **decision tickets** are sub-issues labelled `astack:decision` and one
`decision:<type>`. Bodies and `gh` operations: `../../docs/github.md`.

**Plan, don't do.** Each ticket resolves a decision. The map is done when nothing is left to
decide; then the **spec** skill writes it up and **slice** turns it into buildable work. The pull
to just build it is the sign you've reached the edge of the map.

**Refer by name.** In everything the user reads, call tickets by title with the link inside it.

## The map

The map is an **index**, not a store: a decision lives in exactly one place, its ticket, and the
map only gists it and links. Open tickets are not listed in the map; they are found by query.

- **Ticket or fog?** Ticket a question you can state precisely now, even if it's blocked. Put
  what you can't yet phrase sharply in **Not yet specified**, coarse, not pre-sliced.
- **Out of scope**: work past the destination. Close the ticket and leave one line in **Out of
  scope**. It never graduates back.
- **Blocking** uses GitHub's native blocked-by edges, so the frontier is visible in GitHub.
- **Claim** a ticket by assigning it to the driving user, first, before any work, so parallel
  sessions skip it.

## Ticket types

Each ticket is **HITL** (worked live with the user, who speaks for themselves) or **AFK**.

- `decision:research` (AFK): a fact a decision waits on, from docs, APIs, pricing, or the code.
  Resolved by a **scout** agent (`../../docs/routing.md`), which returns findings with sources;
  post them as the resolution comment.
- `decision:prototype` (HITL): a cheap, rough artifact to react to when "how should it look or
  behave" is the question. Build it with the **tweaker** agent (the **builder** agent for logic
  prototypes) on a throwaway `prototype/<n>-<slug>` branch, push it, link it from the ticket,
  never merge it.
- `decision:grilling` (HITL): conversation, the default. Use the **grill** skill.
- `decision:task` (HITL or AFK): work that must happen before a decision can be made, such as
  signing up for a service or provisioning access. The resolution records what was done and
  any resulting facts later tickets depend on (never secret values).

## Chart a new map

User gives a loose idea.

1. **Name the destination** with the **grill** skill: usually "a spec ready to slice" for one
   project or feature, sometimes a single locked decision. It fixes the scope.
2. **Map the frontier**: grill again breadth-first across the whole space. For a new project,
   cover users and outcome, scope, stack and hosting, data, integrations, auth, development vs
   production, and the riskiest assumption. If no fog appears (the whole thing fits one
   session), you don't need a map: say so and offer **grill** then **spec** instead.
3. **Create the map** issue: Destination and Notes filled, Decisions so far empty, fog sketched.
4. **Create the tickets** you can specify now as sub-issues of the map, then wire blocked-by
   edges in a second pass. Use the **clerk** agent for this when there are three or more.
5. **Fire scouts** in parallel for every new research ticket; post each finding as its
   resolution comment, close it, and add it to Decisions so far.
6. Stop. Charting is one session; it resolves nothing by hand. Tell the user the frontier.

## Work the map

User gives a map. A ticket is optional; without one, you pick.

1. Load the map body, not every ticket body.
2. Take the named ticket, else the first frontier ticket (`../../docs/github.md`). **Claim it.**
3. Resolve it as its `decision:<type>` label says. Read any related or closed ticket on demand.
4. Record it: post the answer as a resolution comment, close the ticket, append a gist and link
   to **Decisions so far**.
5. Create newly surfaced tickets (create, then wire), graduate fog the answer made specifiable,
   and rule anything past the destination out of scope. If the answer invalidates other
   tickets, update or close them.
6. One ticket per session, except research tickets. Expect other sessions editing in parallel.

When the frontier is empty and **Not yet specified** is clear, the map is done: post a closing
comment summarising the route and hand the map to the **spec** skill.
