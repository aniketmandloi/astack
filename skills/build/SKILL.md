---
name: build
description: Build one GitHub issue end to end - claim it, branch, have the right-tier agent implement it test-first, verify, deslop, push, and open a PR that closes it. Use for any feature, slice, UI change, small tweak, or behaviour-preserving refactor. Takes an issue number, a plain description of a small change (it files the issue first), or nothing (it picks the next ready issue).
argument-hint: "[issue | description]"
---

# Build

Turn one issue into one PR. Conventions: `../../docs/github.md`. Routing: `../../docs/routing.md`.

## 1. Pick the issue

- **Issue given**: read it with its comments.
- **Description given**: it must fit one session with no open decisions; otherwise route it
  through the **grill** and **spec** skills first. File it as an `astack:slice` issue with
  acceptance criteria you draft and the user confirms, labelled `status:ready` and a tier.
- **Nothing given**: take the oldest startable `status:ready` issue (no open blocker, no
  assignee) and tell the user which one.

Stop if it has open blockers or someone else's assignee. If it has no testable acceptance
criteria, draft them and get the user's confirmation, then add them to the issue.

## 2. Claim and branch

Claim it (assignee plus `status:in-progress`). Branch `<n>-<slug>` from an up-to-date `main`.
Never build on `main`.

## 3. Implement through the right agent

Send `tier:hard` to the **builder** agent and `tier:small` to the **tweaker** agent; when
unlabelled, judge by the rules in `../../docs/routing.md` and add the label.

**Refactor mode**: when the issue changes structure without changing behaviour (rename,
extract, move, dedupe, simplify, replace an internal API), say so in the brief and send it to
the builder whatever the tier. Its acceptance criteria are "behaviour unchanged, shown by
tests" plus the structural target. In verify, the existing tests must pass without edits.
Any test change needs a reason in the PR, and any behaviour change is split out into its
own issue. Use a **scout**
first if the brief needs facts about the code that you don't have.

The brief opens with the goal in one sentence, then holds: the repo path and branch, the
issue title, body, and acceptance criteria, relevant comments, facts already found, the full
text of `../../docs/slop.md`, whether hands-on checks are `agent` (run end-to-end tests
locally) or not (CI runs them; `../../docs/app-checks.md`), and the instruction to work
test-first, commit each verified step, and return its report. If the tweaker reports the
change is bigger than it looked, re-brief the builder with its findings and relabel
`tier:hard`.

## 4. Verify

Don't trust the report alone. Read the diff against `main`, check each acceptance criterion
against it, and run the project's checks yourself. Send failures back to the same tier with
the output. Check the change for environment leaks: hard-coded URLs or keys, a new variable
missing from `.env.example`, a migration that isn't safe against production. If the change
adds, removes, or changes a project command, or sets a new convention, the AStack block in
`AGENTS.md` must be updated in the same branch (`../../docs/agents-md.md`). If it changes
behaviour that the README or other user-facing docs describe, they are updated in the same
branch too.

## 5. Deslop

A `tier:small` change skips this step: the **review** skill's slop check covers it in the
same independent pass, so a two-line fix gets one review, not two. Run this step for
`tier:hard`, and for any change that touches behaviour across modules, data, auth, or
deployment, whatever its label.

Brief a fresh **builder** agent for a deslop pass. It didn't write the code, so it reads the
diff cold. Give it the branch, the diff against `main`, and the full text of
`../../docs/slop.md`. Send every finding back to the tier that wrote the code, then run the
pass again. Repeat until a pass comes back clean; after two rounds that aren't clean, show the
user what remains and stop. Run the CI gate's commands locally too when the repo has them.
Record the number of rounds and each finding's slop rule for the PR's Deslop section; `retro`
learns from it.

## 6. Open the PR

Push the branch and open a PR with the body from `../../docs/github.md`, written to the prose
rules in `../../docs/slop.md`. Move the issue to `status:in-review`.

## 7. Hands-on checks

For a user-facing change, follow `../../docs/app-checks.md`. Read `ASTACK_APP_CHECKS`, and ask
the user if it's unset. With `agent`, run the checks and post the results. With `manual`, post
the "Checks for you" comment on the issue and link it from the PR. Never start a dev server
unless the user chose `agent`.

Then offer the **review** skill, and run the **babysit** skill so the PR stays green and
conflict-free while it waits.
