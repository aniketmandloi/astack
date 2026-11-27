---
name: babysit
description: Keep an open pull request merge-ready - watch CI, send failures back to the agent that wrote the code, rebase and resolve merge conflicts, and answer review comments - until it is green, conflict-free, and has no unanswered review comments. Never merges. Use after build or fix opens a PR, or for "babysit this PR", "get it green", "fix the conflicts", "address the review comments", "check on this PR".
argument-hint: "[pr] [check]"
---

# Babysit

Conventions: `../../docs/github.md`. Routing: `../../docs/routing.md`.

## Mode

- **drive** (default): loop until the PR is merge-ready or stuck.
- **check**: one status pass and a report, for "check on" or "is it green", and for
  docs-only PRs. It changes nothing.

## Load

Default to the current branch's PR. Read its body, the issue it closes, and that issue's tier
label. The tier names who fixes things: `tier:hard` goes to the **builder**, `tier:small`
to the **tweaker**, and the builder when unlabelled.

## Checkout

Before any edit, rebase, or push, make sure the local checkout is this PR. The PR named may
not be the branch the user is on.

1. Read `gh pr view <pr> --json headRefName,headRefOid,headRepository,headRepositoryOwner,isCrossRepository,maintainerCanModify`.
   The PR's head lives at `<headRepositoryOwner.login>/<headRepository.name>`, which isn't
   necessarily `origin`.
2. A fork PR (`isCrossRepository`) can be pushed to only when `maintainerCanModify` is true.
   Otherwise, run **check** mode and comment on the PR with what the author needs to change.
3. Compare with the local state (`git branch --show-current`, `git status --porcelain`).
   - **Uncommitted changes**: never stash, reset, or discard them. Stop and ask the user to
     commit them, stash them, or have the PR worked in a separate worktree. In astack mode,
     this goes to Waiting on you, and the run moves on to units that don't need the checkout.
   - **Clean, but on another branch**: `gh pr checkout <pr>`.
4. `git fetch origin`. Local `HEAD` must equal `headRefOid`. If the remote moved ahead,
   `git pull --ff-only`. If the two have diverged, stop and report it.
5. **Find the head remote.** It's the remote whose URL (`git remote -v`) points at
   `<headRepositoryOwner.login>/<headRepository.name>`. For a same-repo PR that's usually
   `origin`. For a fork PR, `gh pr checkout` adds it. With no matching remote, stop and
   report: a push anywhere else would create a stray branch and leave the PR untouched.
6. Every push goes to that verified `<head-remote>`, and names the branch and the commit it
   expects to replace: `git push <head-remote> HEAD:<headRefName>`, or after a rebase,
   `git push --force-with-lease=<headRefName>:<oid-before-rebase> <head-remote> HEAD:<headRefName>`.

## Drive loop

Work one problem at a time, in this order, then wait for checks with
`gh pr checks <pr> --watch`, and repeat.

1. **Conflicts** (`gh pr view <pr> --json mergeable,mergeStateStatus`). Rebase on the latest
   `main`: `git fetch origin && git rebase origin/main`. Resolve purely mechanical conflicts
   yourself, such as imports, lockfiles, or adjacent edits. Send any conflict that touches
   logic to the builder, with both sides and the issue's goal. Rerun the project's checks,
   then push to the verified head remote with the explicit lease from Checkout step 6.
2. **Red checks** (`gh pr checks <pr>`). Read the failure with `gh run view <run-id>
   --log-failed`. If it looks flaky, rerun it once (`gh run rerun <run-id> --failed`). The same
   failure twice is real: brief the tier with the log and the goal.
3. **Review comments**: every unanswered comment, whether from the **review** skill, a human,
   or a bot. Judge each on its merits. Fix a real problem through the tier. Answer noise with
   a concrete reason in a reply, and change no code for it. Never dismiss a human's review.

Every fix passes the **build** skill's verify and deslop steps before it is pushed.

## Done or stuck

- **Merge-ready**: checks green, mergeable, every review comment answered, and a "ready" review
  verdict whose `Reviewed at` SHA is the current head. If babysit pushed after the last review,
  run the **review** skill first. It reviews only the new commits, and after a plain rebase it
  confirms there's no content change without reviewing anything. If a fix changed what the PR
  description says (files, behaviour, or risk), rerun the **pr** skill to edit the body. Report
  the SHA it's ready at. Merging follows `../../docs/github.md`: the user's go-ahead, or the
  astack mode gates.
- **Stuck**: the same failure after two fix rounds, or a conflict that needs a product
  decision. Comment on the PR with what was tried and what's needed, then stop.

Never push to `main`, merge, or force-push without `--force-with-lease`.
