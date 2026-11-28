---
name: review
description: Review a change against the GitHub issue it closes - acceptance criteria, tests, correctness, blast radius, security, development/production safety, and slop - in a fresh context, either here or in another CLI (Codex or Claude Code) that the user runs and pastes back. Runs before a PR exists (build and fix call it on the local branch, so CI runs once) or on an open PR. A re-review checks only the commits since the last review and whether each earlier finding is fixed. Use after build or fix, or when the user asks to review a branch or PR.
argument-hint: "[pr | branch]"
---

# Review

Conventions: `../../docs/github.md`. Routing: `../../docs/routing.md`.

## Modes

- **Branch** (before a PR exists): `build` and `fix` run review on the local branch before
  anything is pushed. A PR then opens only once the review is clean, so CI runs once rather
  than once per round of fixes. The result goes back to the caller, which posts it when the
  PR opens.
- **PR**: an open PR. Default to the current branch's PR. The result is posted on the PR.

## 1. Choose the scope

Read the head commit SHA: `git rev-parse HEAD` for a branch, or `gh pr view <pr> --json
headRefOid` for a PR. Then compare it with the last review, if there is one: the previous
result passed in by the caller, or the PR's last `Reviewed at <sha>` comment.

| Situation | Scope |
|---|---|
| No earlier review | **Full**: the whole diff against the merge base with `main` |
| Earlier review, and new commits after it | **Delta**: only `git diff <reviewed-sha>..HEAD`, plus a check that each earlier finding is now fixed |
| Earlier review, and only a rebase since | **Rebase**: `git range-diff <old-base>..<reviewed-sha> <new-base>..HEAD`. If it shows no content change beyond the new base, there's nothing to review. Record `Reviewed at <new-sha> by <the earlier reviewer> (rebase only, no changes)` |
| The delta is larger than half the original diff, or rewrites the approach | **Full** again |

A delta review costs a fraction of a full one. Never re-review the whole PR just because one
finding was fixed.

## 2. Review in a fresh context

### Who reviews

The reviewer is either **here** (this session's builder agent) or **another CLI** (Codex
from Claude Code, or Claude Code from Codex) that the user runs and relays. Take the choice
from the caller when it passes one (mode passes the run's Grant). Otherwise:

- **PR mode**: reuse the reviewer named in the PR's last `Reviewed at` comment. This
  session's own CLI means here; the other one means another CLI. Ask only when there's none.
- **Branch mode**: ask once per issue: "Review here, or in another CLI?" Later rounds for the
  same issue reuse the answer.

### Here

Brief the **builder** agent in review mode, so the reviewer isn't the author. Give it the
scope from step 1, the issue's acceptance criteria, the earlier findings for a delta review,
and this checklist:

- each acceptance criterion: met, with the code or test that shows it, or not met
- tests: they test behaviour, fail without the change, and cover the edge cases the issue names
- correctness: concrete inputs that break it
- blast radius: the callers, consumers, jobs, and data outside the diff that depend on what
  changed. For each one, show why it's safe by naming the test that covers it, or by running
  it. "Looks fine" doesn't count
- security: secrets in code or logs, injection, missing authorization, unsafe input handling
- environments: hard-coded environment values, variables missing from `.env.example`,
  migrations unsafe against production, config that only works in one environment
- slop: every rule in `../../docs/slop.md` (include its full text), in the code and, in PR
  mode, the PR body

In a delta review, the checklist applies to the delta. Each earlier finding is marked fixed,
with the commit that fixed it, or still open.

The reviewer reports findings with file:line and the failure each causes or the slop rule it
breaks. Drop any finding it can't tie to one of those.

### In another CLI

The other CLI runs with the user, so it gets the same brief as a file, and its reply comes
back through the user.

1. Write the brief to the path `git rev-parse --git-path astack/review-<branch>.md` prints,
   creating its directory first. That path is inside `.git`, so it's never committed, and it
   stays correct in a worktree. The brief holds everything the builder brief above holds,
   plus: the branch, the head SHA, the issue body, the PR body in PR mode, and "Don't edit
   files, commit, or post to GitHub. Reply in exactly this format:"

   ```
   Reviewed at <head-sha> by <your CLI> (<full | delta>)
   Verdict: <ready | changes needed>
   Earlier findings: <each one: fixed in <sha>, or open>
   1. <file>:<line>: <what's wrong>. <Failure: the concrete break | Slop rule: <n>>
   ```

   The other CLI may have no network access, so the brief carries the issue and earlier
   findings itself rather than pointing at GitHub.
2. Tell the user, with the brief's absolute path: "Paste this into Codex (or Claude Code),
   started in this repo: `Read <path> and follow it.` Then paste its whole reply here." For a
   delta round, suggest the same session of the other CLI.
3. Check the pasted reply before using it. Its SHA must be the current head and its scope
   the one from step 1; otherwise say which commit it covers and ask for a fresh run. Drop any
   finding without a file:line and a failure or slop rule, as above.
4. In mode, the review becomes a Waiting on you item holding that one-line prompt. The run
   carries on with other units until the user pastes the reply.

## 3. Verdict

The verdict is **ready** or **changes needed**. Any slop finding, any unmet criterion, or any
open earlier finding means changes needed. A slop finding is never left as a nit. In PR mode,
a red check is also a finding (`gh pr checks <pr>`).

The result opens with `Reviewed at <sha> by <reviewer>` and the scope (full, delta, or
rebase), then the verdict, then the findings, most severe first. The reviewer is the CLI that
did the review (`claude-code` or `codex`), so a later round can reuse it. The verdict covers
only that commit.

## 4. Deliver it

- **Branch mode**: return the result to the caller. On changes needed, the caller sends the
  findings to the tier that wrote the code, then calls review again, which runs as a delta.
- **PR mode**: post it once with `gh pr review <pr> --comment`. A solo author can't approve
  their own PR, so the verdict goes in the comment. On changes needed, run the **babysit**
  skill, which works through the findings with the tier that wrote the code. On ready, tell the
  user. Merge only on their explicit go-ahead, pinned to the reviewed commit, then watch the
  deploy of the merge commit (`../../docs/github.md`, "Commits, verdicts, and deploys"). The
  issue closes through `Closes #<n>`.
