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

## Drive loop

Work one problem at a time, in this order, then wait for checks with
`gh pr checks <pr> --watch`, and repeat.

1. **Conflicts** (`gh pr view <pr> --json mergeable,mergeStateStatus`). Rebase on the latest
   `main`: `git fetch origin && git rebase origin/main`. Resolve purely mechanical conflicts
   yourself, such as imports, lockfiles, or adjacent edits. Send any conflict that touches
   logic to the builder, with both sides and the issue's goal. Rerun the project's checks,
   then `git push --force-with-lease`, only ever to the PR's own branch.
2. **Red checks** (`gh pr checks <pr>`). Read the failure with `gh run view <run-id>
   --log-failed`. If it looks flaky, rerun it once (`gh run rerun <run-id> --failed`). The same
   failure twice is real: brief the tier with the log and the goal.
3. **Review comments**: every unanswered comment, whether from the **review** skill, a human,
   or a bot. Judge each on its merits. Fix a real problem through the tier. Answer noise with
   a concrete reason in a reply, and change no code for it. Never dismiss a human's review.

Every fix passes the **build** skill's verify and deslop steps before it is pushed.

## Done or stuck

- **Merge-ready**: checks green, mergeable, every review comment answered, and the review
  verdict "ready". Report it. Merging follows `../../docs/github.md`: the user's go-ahead,
  or the astack mode gates.
- **Stuck**: the same failure after two fix rounds, or a conflict that needs a product
  decision. Comment on the PR with what was tried and what's needed, then stop.

Never push to `main`, merge, or force-push without `--force-with-lease`.
