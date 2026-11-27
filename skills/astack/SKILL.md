---
name: astack
description: Start here for any software work in a GitHub repo - starting a new project, adding a feature, changing the UI, fixing a bug, making a small tweak, reviewing a PR, releasing, or asking "what's next". Reads the repo's GitHub issues and PRs to find where work stands and routes to the right AStack skill (chart, grill, spec, slice, build, fix, review, pr, babysit, triage, retro, help, setup, ship, mode).
argument-hint: "[what you want to do]"
---

# AStack

AStack keeps all state on GitHub (`../../docs/github.md`) and routes work by difficulty to
pinned models (`../../docs/routing.md`). Any request can enter here, at any stage.

## 1. Orient

Send a **scout** agent to report, read-only:
- the repo (`gh repo view --json nameWithOwner,visibility`) and whether AStack is set up,
  from `gh variable get ASTACK_SETUP`:
  - `complete`: set up.
  - `awaiting-merge`: set up only once the `astack-setup` PR has merged and its files are on
    the default branch. If they are, set the variable to `complete`. If the PR is still open,
    the next step is the user merging it. If it closed unmerged, setup needs a rerun.
  - unset with AStack labels present: an interrupted setup.
- open `astack:map`, `astack:spec`, `astack:slice`, and `astack:bug` issues, with status,
  tier, and assignee
- open PRs and their check status, and whether the repo has application code yet

Skip it when the request already names an issue or PR and the repo is known to be set up.

## 2. Route

| Situation | Route |
|---|---|
| Not set up, or setup interrupted | Tell the user to run `/astack:setup` (Codex: `$setup`); it resumes an interrupted setup, and it changes repo settings, so only they start it |
| New project, or an effort too big or foggy for one session | **chart** → **spec** → **slice** |
| A feature with open decisions that fits one session | **grill** → **spec** → **slice** |
| A clear feature, UI change, or tweak that fits one session | **build** (it files the issue first) |
| Open issues with no `astack:` label, or customer feedback | **triage** |
| A bug, error, or regression | **fix** |
| A refactor or cleanup that keeps behaviour the same | **build**, in refactor mode |
| A map with open tickets | **chart** on that map |
| A spec with no Slice plan, or one with unticked items | **slice** |
| A reviewed branch with no PR, "open a PR", or "update the PR description" | **pr** |
| An open PR awaiting review, or "review this" | **review** |
| A PR with red checks, conflicts, or unanswered comments | **babysit** |
| "What's next?" or no request | **build** on the next startable slice; otherwise the next frontier ticket of an open map |
| Release or deploy to production | Tell the user to run `/astack:ship` (Codex: `$ship`) |
| A spec whose slices are all closed with no retro yet, or "retro" | **retro** |
| A question about AStack, or "where am I?" without wanting work started | **help** |
| "Do it all yourself", "run until done" | Tell the user to run `/astack:mode <goal>` (Codex: `$mode`); only they can grant it |

When two rows fit, take the earlier stage: unsettled decisions come before building.

## 3. Go

State the route in one line, with the issue or PR by title and link, then load that skill and
follow it. Before any code is written, the work has an issue. The only exceptions are
questions and prototype tickets.
