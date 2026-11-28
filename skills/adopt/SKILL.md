---
name: adopt
description: Bring an existing project into AStack when its code is ahead of its GitHub issues - after BMAD, Spec Kit, pstack, gstack, or no workflow at all. Reads the code, the git history, and whatever planning files the old workflow left, files a closed baseline spec of how the system works today, turns unfinished work into specs, slices, or issues for triage, and offers one PR for old rules and planning files. Deletes nothing. Use once after setup on a repo with code but no AStack issues, or when the user is moving from another workflow; rerun it to import sources added since.
argument-hint: "[paths to planning files]"
disable-model-invocation: true
---

# Adopt

Conventions: `../../docs/github.md`. Routing: `../../docs/routing.md`.

Scouts gather the facts. This session decides what each item becomes and writes the
baseline, as it would a spec. The clerk does bulk issue writes.

## 1. Check the repo

- `gh variable get ASTACK_SETUP` must read `complete`. Otherwise tell the user to run
  `/astack:setup` (Codex: `$setup`) and stop.
- Look for an earlier baseline: `gh issue list --state all --label astack:spec --search
  "Baseline: in:title" --json number,title,body`. If there is one, this is a rerun. Its
  Sources imported list says what's done, so import only sources that are new or changed
  since the commit it records, and update that baseline instead of filing a second one.
- Read the default branch's head commit. Everything below describes that commit, and every
  source link is a permalink at it (`../../docs/github.md`, "Baseline").

## 2. Find what the old workflow left

Send scouts in parallel. Each labels every claim measured (seen in the code), documented
(only in a doc), or inferred, with its source.

- **Planning files**, recognised by their content: a PRD or brief, an architecture doc,
  epics, stories with a status and acceptance criteria, task lists, ADRs, roadmaps, TODO
  files. Start with the paths the user passed and the places below, but search beyond them,
  because layouts change between versions:

  | Workflow | Start at |
  |---|---|
  | BMAD v6 | `_bmad-output/planning-artifacts/`, `_bmad-output/implementation-artifacts/` |
  | BMAD v4 | `docs/`: the PRD, the architecture doc, `docs/stories/` |
  | Spec Kit | `.specify/memory/constitution.md`; `specs/*/` or `.specify/specs/*/` (`spec.md`, `plan.md`, `tasks.md`) |
  | Any | `docs/adr/`, `ROADMAP.md`, `TODO.md`, `PLAN*.md`, Markdown with acceptance criteria or task checkboxes |

  pstack, gstack, and many setups leave no planning files. Then the code and its history
  are the whole source, and the baseline is still complete.
- **Rules**: `CLAUDE.md`, `AGENTS.md` outside the AStack block, `.cursor/rules/`,
  `.cursorrules`, a Spec Kit constitution, coding-standards docs.
- **Work in flight**: branches not merged into the default branch, open PRs, and open issues
  with no `astack:` label.
- **The system**: what it does, its areas, key files, data model, interfaces, external
  services, commands, deploy target, and the tests that cover each area. Use one scout per
  top-level area in a large repo. Commit messages, merged PR bodies, and closed issues with
  the PRs that closed them often record why a decision was made.

## 3. Check every plan against the code

For each planned item (story, task, epic, roadmap line) and each open issue with no
`astack:` label, a scout reports **built** (the code or test that shows it; for a bug, that
it's fixed), **partly built** (what's there and what's missing), or **not built**.
Where a doc and the code disagree, the code is what runs. Record the conflict.

## 4. Decide what each item becomes

| Found | Becomes |
|---|---|
| Built work and done stories | A line in the baseline, never one closed issue per story |
| Unfinished stories of an epic whose decisions the docs settle | An open `astack:spec` for the epic, filled from its docs, with Open questions empty. Each story becomes an `astack:slice` sub-issue with `status:ready` and a tier. Its acceptance criteria come from the story, cut to what's still missing when it's partly built |
| A single settled item | A standalone `astack:slice` with `status:ready` and a tier |
| Anything with open decisions, or too vague to slice | A plain issue with no `astack:` label, quoting its source. **triage** sorts it next, into chart, grill, or a slice |
| An open branch or PR | Linked from the issue it belongs to. One that matches nothing is listed for the user |
| An open issue with no `astack:` label | Stays where it is, never refiled. Built or fixed: a closing comment naming the code or test, for the user to approve. Otherwise **triage** labels it in place |
| `TODO` comments | Not filed. Counted under Known gaps and offered to triage as a list |
| Slop in existing code | When the repo has the gate's linter and unused-code tools (`../../docs/slop.md`, "CI gate"), run them over the whole codebase. The hits become one `astack:slice` cleanup in refactor mode, so turning on `ci` later doesn't block on old code. Without the tools, note it under Known gaps |

Before filing anything, match it against the repo's issues, open and closed. A match gets a
comment linking the source instead of a new issue.

An epic with an open decision isn't a spec yet. Send its open decisions to triage as above,
and file slices only for the stories that are settled.

## 5. Preview

Before writing anything, show one table: the baseline's sections, each issue with its kind,
title, and source, each existing issue to close with the code that does it, and each
conflict. List the file changes from step 7 separately, as their
own opt-in. For each conflict, ask: the code wins, unless the user says the doc describes
what they want, and then it becomes a bug or a slice. Apply only what the user approves.

## 6. Write it on GitHub

- File the specs, slices, and plain issues first, through the **clerk** when there are three
  or more. Each body ends with `Imported from <permalink>`. Wire sub-issues and blocked-by
  edges in a second pass. Comment on the matched existing issues, and comment on, then close,
  the existing issues the user agreed are done.
- Then file the baseline (body in `../../docs/github.md`), so its Sources imported list can
  link the issues each source became. Close it with a comment that lists what was imported.
- On a rerun, update the baseline's sections and its Sources imported list, and comment what
  changed.

## 7. Old files, only if the user agrees

Offer one PR on branch `astack-adopt`:
- Rules from `.cursor/rules`, a constitution, or coding-standards docs move into `AGENTS.md`
  above the AStack block, the part that belongs to the user (`../../docs/agents-md.md`).
  Never into the block, which setup rewrites, and never into Pitfalls, which only retro
  writes.
- Each imported planning file is replaced by one line linking to the issue it became.

The old workflow's own tooling (`_bmad/`, Spec Kit's templates and scripts, installed skills)
is listed in the report and left alone. Merging the PR is the user's call. If they decline,
every file stays as it is.

## 8. Report

- the baseline, with its link
- what was filed, counted by kind, with links, and the existing issues closed or matched
- each conflict and how it was resolved
- the old-files PR, or "files unchanged"
- what remains unverified: every claim labelled documented

Then the next step: **triage** while any open issue has no `astack:` label (plain issues
adopt filed, or ones that were already there), then **build** on the oldest ready slice, or
`/astack:mode <goal>`.
