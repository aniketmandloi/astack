---
name: help
description: Answer any question about AStack (what a skill does, how the flow works, model routing, environments, slop rules, astack mode, setup and install) and tell the user exactly what to do next in the current repo, from its GitHub state. Read-only, never starts work. Use for "astack help", "what do I do next", "where am I", "how does astack work", or any question about AStack.
argument-hint: "[question]"
---

# AStack help

Answer questions and point to the next step. Change nothing: no file edits, and no `gh`
command that writes. When the user wants something done, give the command that does it.

## Questions about AStack

Answer from AStack's own files, never from memory. Read the ones the question touches, quote
or paraphrase them, and name the file.

| Question about | Read |
|---|---|
| The overall flow, install, the list of skills | `../../README.md` |
| A specific skill | `../<skill>/SKILL.md` (astack, mode, setup, adopt, chart, grill, spec, slice, build, fix, review, pr, babysit, triage, retro, ship) |
| Moving an existing project in from BMAD, Spec Kit, pstack, gstack, or no workflow | `../adopt/SKILL.md` |
| Testing the running app, hands-on checks, `ASTACK_APP_CHECKS` | `../../docs/app-checks.md` |
| The guard that blocks destructive commands | `../../docs/autonomy.md`, `../../hooks/guard.py` |
| Labels, issue bodies, branches, PRs | `../../docs/github.md` |
| Which model does what | `../../docs/routing.md`, `../../agents/` |
| Development vs production, CI/CD, secrets, plans | `../../docs/environments.md` |
| Slop, code rules, the CI gate | `../../docs/slop.md` |
| Launch readiness, the first customer | `../../docs/launch.md` |
| `AGENTS.md` and `CLAUDE.md` in projects | `../../docs/agents-md.md` |
| What astack mode decides and when it pauses | `../../docs/autonomy.md` |
| What setup changes, keeping an existing GitHub setup, Light/Custom/Full | `../../docs/footprint.md` |

If the files don't answer it, say so plainly rather than filling the gap.

## What to do next

Send a **scout** agent (`../../docs/routing.md`) for the repo's state, read-only:
- whether AStack is set up (`gh variable get ASTACK_SETUP`): `complete` means set up;
  `awaiting-merge` means the `astack-setup` PR still needs merging; unset with AStack labels
  means setup was interrupted, and rerunning `/astack:setup` resumes it
- what AStack manages here (`gh variable get ASTACK_MANAGES`, `../../docs/footprint.md`)
- an open `astack:run` issue, with its Waiting on you
- open `astack:map`, `astack:spec`, `astack:slice`, `astack:bug`, and `astack:launch` issues,
  with status, tier, assignee, and open blockers
- open PRs, with check status and review verdict
- the latest `main` CI run and development deploy, and the last release

Then answer in this order, using issue and PR titles with their links:

1. **Where you are**: the stage in the flow (setup, chart, spec, slice, build, release) in
   one or two sentences.
2. **Waiting on you**: everything only the user can do right now. That covers issues assigned
   to them, user-work slices, HITL decision tickets, PRs ready to merge, production approvals,
   secrets to set, and the run issue's Waiting on you. Give each with its exact command or
   the place in GitHub to do it.
3. **Next command**: the one command to run next and what it will do, plus
   `/astack:mode <goal>` when the rest could run on its own.

Not a git repo, or no GitHub remote: say so and give the first steps from the README
(create the repo, then `/astack:setup`).
