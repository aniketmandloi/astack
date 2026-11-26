---
name: slice
description: Break a spec issue into vertical-slice sub-issues on GitHub, each with testable acceptance criteria, blocked-by links, and a tier label that routes it to the right model. Use after a spec is filed, or when the user wants a feature broken into tickets.
argument-hint: "<spec issue>"
---

# Slice

Turn an `astack:spec` issue into buildable work: `astack:slice` sub-issues with the body in
`../../docs/github.md`.

## What a slice is

- **Vertical**: a thin path through every layer it touches (UI, API, data, tests), demoable on
  its own. Never "do the database layer" then "do the API".
- **One session**: one agent can build, test, and open a PR for it in a single session.
- **Independently mergeable**: `main` stays deployable after each one merges.
- **Testable**: its acceptance criteria come from the spec's Behaviour and can each be checked
  by a test or a stated manual check.

For a new project, the first slice is the **walking skeleton**: scaffold the app with the
framework's official generator, add the health endpoint, one passing test, and the baseline in
`../../docs/environments.md`, plus whatever `setup` deferred: the `ci.yml` and `deploy.yml`
workflows with the slop gate, the package ecosystem in `dependabot.yml`, and the Commands and
Conventions sections of the AStack block in `AGENTS.md` (`../../docs/agents-md.md`), so that
merging it deploys to development. Every other slice is blocked by it.

The walking skeleton is itself blocked by a user-work slice, **Connect hosting**. In it the
user creates the host project for development and for production, and sets each deploy
secret with `gh secret set <NAME> --env <environment>`. The slice body names every secret
the deploy workflow will read. It is assigned to the user and has a checklist body.

When the spec has a Launch section, each item's work becomes a slice that also carries
`astack:launch`, as `../../docs/launch.md` describes. Build work is a normal slice with a tier.
User work is assigned to the user and has a checklist body instead of acceptance criteria.

## Tier

Label each slice for routing (`../../docs/routing.md`):

- `tier:hard`: new modules or architecture, changes across modules, tricky logic, data
  migrations, auth or payments, the walking skeleton.
- `tier:small`: contained in a few files with no design decision: copy, styling, small UI
  changes, config, a field added along an existing path.

## Steps

1. Read the spec (and its parent map if it has one). Stop and offer the **grill** skill if its
   Open questions aren't empty.
2. Use a **scout** agent to learn the current code's structure where slices touch it.
3. Draft the slices in build order: title, one-line what, acceptance criteria, tier, and what
   each is blocked by. Present the list to the user and apply their changes before creating
   anything.
4. Create them with the **clerk** agent: each issue labelled `astack:slice`, `status:ready`,
   and its tier; then, in a second pass, link each as a sub-issue of the spec and wire its
   blocked-by edges. Give the clerk the exact bodies and the operations from
   `../../docs/github.md`.
5. Report the slices by title with links, and which are startable now. Offer the **build**
   skill on the first one.
