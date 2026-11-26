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

Merging it delivers to development.

Two user-work slices go with it. Each is assigned to the user, and each has a checklist body
that names every secret the workflow will read, already written in the form for the repo's
`ASTACK_SECRETS_MODE` (`../../docs/environments.md`):
- **Connect development**: only what the development channel needs (a host project, a test
  track, or a registry token), plus its secrets.
- **Connect production**: the same for production. It's labelled `astack:release`.

A new project's blocked-by edges follow exactly this order:

```
Connect development  →  walking skeleton  →  every application slice
Connect production   (no edges; ship requires it closed)
```

Connect development blocks only the skeleton. The skeleton blocks every other buildable slice.
Connect production neither blocks nor is blocked, so production provisioning can wait until
the first usable flow works.

When the spec has a Launch section, each item's work becomes a slice that also carries
`astack:launch`, as `../../docs/launch.md` describes. Build work is a normal slice with a tier.
User work, such as buying the domain or activating live payments, is assigned to the user,
has a checklist body instead of acceptance criteria, and is also labelled `astack:release`
because it only has to be done before a release.

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
4. **Post the plan** as a comment on the spec headed `## Slice plan`. It holds everything
   approved, so a fresh session can recreate any slice from it alone. Each slice gets a stable
   id, `S1`, `S2`, and so on:

   ```markdown
   - [ ] **S2** <title> · tier:hard · blocked by: S1
     - What: <one line>
     - Criteria: <criterion>; <criterion>
   ```

   User-work slices list their checklist instead of criteria, and their labels
   (`astack:release`) instead of a tier. The comment records progress.
5. Create the slices with the **clerk** agent: each issue labelled `astack:slice`,
   `status:ready`, and its tier; then, in a second pass, link each as a sub-issue of the spec
   and wire its blocked-by edges. Give the clerk the exact bodies and the operations from
   `../../docs/github.md`. Tick a plan item, adding the issue link, only once that slice is
   created, linked, and wired.
6. Report the slices by title with links, and which are startable now. Offer the **build**
   skill on the first one.

**Resuming**: if the spec already has a Slice plan with unticked items, skip drafting. For
each unticked item, look for an issue that was already created. It counts only if its body
starts with this spec's `Part of` link and carries the same `Plan item: S<n>` line. Titles
alone don't count, because another spec can have a slice with the same title. Finish
whatever it's missing (creation from the plan's recorded fields, the sub-issue link, or the
edges), then tick the item. A spec is fully sliced only when every item of its plan is ticked.
