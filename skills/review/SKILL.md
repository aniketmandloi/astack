---
name: review
description: Review an open pull request against the GitHub issue it closes - acceptance criteria, tests, CI, security, development/production safety, and slop - and post the findings on the PR. Use when a PR is ready for review, after build or fix, or when the user asks to review a PR.
argument-hint: "[pr]"
---

# Review

Conventions: `../../docs/github.md`. Routing: `../../docs/routing.md`.

1. **Load** the PR (default: the current branch's PR): body, diff, `gh pr checks`, and the
   issue it closes with its acceptance criteria.
2. **Review in a fresh context.** Brief the **builder** agent in review mode, so the reviewer
   isn't the author. Give it the PR number, the issue's acceptance criteria, and this list:
   - each acceptance criterion: met, with the code or test that shows it, or not met
   - tests: they test behaviour, fail without the change, and cover the edge cases the issue names
   - correctness: concrete inputs that break it
   - blast radius: the callers, consumers, jobs, and data outside the diff that depend on what
     changed. For each one, show why it's safe by naming the test that covers it, or by
     running it. "Looks fine" doesn't count
   - security: secrets in code or logs, injection, missing authorization, unsafe input handling
   - environments: hard-coded environment values, variables missing from `.env.example`,
     migrations unsafe against production, config that only works in one environment
   - slop: every rule in `../../docs/slop.md` (include its full text), in the code and in the
     PR body
   It reports findings with file:line and the failure each causes or the slop rule it breaks.
   Drop any finding it can't tie to one of those.
3. **Check CI** yourself. A red check is a finding. Any slop finding means "changes needed";
   it is never left as a nit.
4. **Post** one PR comment with `gh pr review <pr> --comment`: verdict (ready to merge, or
   changes needed), then findings, most severe first. A solo author can't approve their own PR,
   so the verdict goes in the comment.
5. **Changes needed**: offer the **babysit** skill, which works through the findings with the
   tier that wrote the code. **Ready**: tell the user it's ready. Merge only on their explicit go-ahead, with
   `gh pr merge --squash`. The issue closes through `Closes #<n>`.
