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
  by a test or a stated manual check. A user-facing slice includes an end-to-end test of its
  main flow.

For a new project, the first slice is the **walking skeleton**: the thinnest version of the
spec's artifact that reaches the development channel for its kind (see "Artifact kinds" in
`../../docs/environments.md`). It includes:
- the app scaffolded with the framework's official generator, using non-interactive flags
- one passing test
- the end-to-end harness, with one smoke test against that exact artifact
  (`../../docs/app-checks.md`)
- the baseline in `../../docs/environments.md` that applies to its kind, such as a health
  endpoint for a hosted app
- whatever `setup` deferred: the `ci.yml` and `deploy.yml` workflows with the slop gate, the
  package ecosystem in `dependabot.yml`, and the Commands and Conventions sections of the
  AStack block in `AGENTS.md` (`../../docs/agents-md.md`)

Merging it delivers to development. Every other slice is blocked by it.

The walking skeleton is itself blocked by a user-work slice, **Connect development**. In it the
user sets up only what the development channel needs (a host project, a test track, or a
registry token), and sets each secret with the command for the repo's `ASTACK_SECRETS_MODE`
(`../../docs/environments.md`). A second user-work slice, **Connect production**, does the
same for production. It blocks no slice, but `ship` won't release until it's closed, so
production provisioning can wait until the first usable flow works. Each body names every
secret the workflow will read, already written in that mode's form, and each is assigned to
the user with a checklist body.

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
4. **Post the plan** as a comment on the spec headed `## Slice plan`. Each slice gets one
   line: `- [ ] <title>: <one-line what> (blocked by: <titles>)`. This comment records
   progress.
5. Create the slices with the **clerk** agent: each issue labelled `astack:slice`,
   `status:ready`, and its tier; then, in a second pass, link each as a sub-issue of the spec
   and wire its blocked-by edges. Give the clerk the exact bodies and the operations from
   `../../docs/github.md`. Tick a plan line, adding the issue link, only once that slice is
   created, linked, and wired.
6. Report the slices by title with links, and which are startable now. Offer the **build**
   skill on the first one.

**Resuming**: if the spec already has a Slice plan with unticked lines, skip drafting. For
each unticked line, find any issue that was already created (by title, among the spec's
sub-issues and open `astack:slice` issues). Finish whatever it's missing (creation, link, or
edges), then tick the line. A spec is fully sliced only when every line of its plan is ticked.
