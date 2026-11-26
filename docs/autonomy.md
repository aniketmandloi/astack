# Autonomy

The rules `/astack:mode` runs under. Typing `/astack:mode` grants everything under
**Decides** for that run and nothing under **Always pauses**. The user can narrow the grant
in the same message ("plan only", "don't merge", "stop after the spec"), and the narrowing
is recorded in the run issue.

## Decides, and records

- **Grilling questions**: takes its own recommended answer. This overrides chart's rule that
  HITL tickets resolve only live with the user; the user's override comes afterwards.
- **Prototype tickets**: judges the prototype against what can be observed. On taste alone,
  takes the conventional choice for the product's kind.
- **Drafts**: files specs, slice lists, and acceptance criteria without waiting for approval.
- **Merging**: merges a PR into `main` (rebase when allowed, `docs/footprint.md`) when, at its
  current head commit, its checks are green (the `ci` check, when AStack manages CI), the deslop pass is clean (for a `tier:small` change, which skips that pass, the
  review's slop check stands in), and the review verdict is "ready". The merge is pinned to
  that commit with `--match-head-commit` (`docs/github.md`). This deploys to development only.
- **Routine GitHub work**: issues, labels, branches, PRs, comments, agent spawns.

Every skill step that says "show the user", "get the user's confirmation", or "wait" becomes
"decide, record, continue" in a run, except for the list below.

## Always pauses

These go to **Waiting on you** in the run issue. The run keeps working on anything they
don't block, and stops only when everything left waits on the user.

- **Production**: creating a release, approving a production deploy, changing production
  settings.
- **Money and accounts**: buying a domain, paid plans, signing provider terms, live payments.
- **Secrets**: their values, which only the user sets.
- **Destructive actions**: deleting data, branches, or issues; force-pushes; migrations that
  drop or rewrite existing data.
- **Outside people**: any message to customers or anyone else outside the repo.
- **Calls only the user can make**: who the first customer is, pricing, legal text, the
  product's name and brand, and anything the user has said they'll decide.
- **Reversing a user decision**: anything that contradicts what the user decided earlier.
- **Repo setup**: `/astack:setup` is the user's to run.
- **Hands-on checks** (`docs/app-checks.md`): with `ASTACK_APP_CHECKS` unset, the run uses
  `manual` and adds the question to the list. Each "Checks for you" comment joins the list
  too, and the change still merges to development, where the checks are run.

In Claude Code, the AStack guard hook (`hooks/guard.py`) backs up the destructive part of
this list for shell commands. The README lists exactly what it denies. It can't see GitHub
settings, ORM migration CLIs, or anything outside the agent's shell, so the rules above still
apply in full. The user can run any blocked command with `! <command>`. Codex runs plugin hooks only in manually installed desktop plugins, so
there the instructions are the only guard.

## Recording

- Each decision is posted where it would have been recorded anyway: a resolution comment,
  the spec, the slice, or the PR. It opens with **Decided by astack mode** and gives the
  answer, a one-line reason, and "Reply here to override." Lines it adds to a map's
  Decisions so far end with "(auto)".
- Each run has one tracking issue labelled `astack:run`:

```markdown
## Goal
<one sentence: what the run gives its user, and the smallest outcome that meets it>

## Grant
<the default grant, plus any narrowing the user gave>

## Scope
- [<map, spec, or issue that holds the goal>](<url>)
- [<issue the run filed>](<url>): <why it was filed>

## Progress
- [<issue or PR title>](<url>): <state>

## Decided by astack mode
- [<where it was recorded>](<url>): <one-line gist>

## Waiting on you
- [ ] <action, with the link and the exact command or place to do it>
```

- An override reply on any "Decided by astack mode" item turns it into the user's decision.
  The next run reopens or updates whatever depended on it.
