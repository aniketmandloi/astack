# Footprint

How much of a repo's GitHub setup AStack may change. A team can use AStack to plan and build
features without letting it touch their workflows, settings, or rules. `setup` asks, and
records the answer in the repo variable `ASTACK_MANAGES`: a comma-separated list of the items
below. Every other skill reads it and adapts.

## Items

| Item | What AStack adds | What it gives |
|---|---|---|
| `labels` | the labels in `docs/github.md`, always | issues, maps, specs, and slices AStack can track. Required |
| `agents-md` | the AStack block in `AGENTS.md`, and the `@AGENTS.md` import in `CLAUDE.md` | plain sessions follow the same rules |
| `templates` | issue and PR templates, only when the repo has none | people filing issues use AStack's shapes |
| `ci` | the `ci` workflow and the slop gate | CI enforces tests and slop rules |
| `deploy` | the deploy workflow, the `development` and `production` environments, and the secrets mode | automatic development deploys, `ship`, and rollback |
| `merge` | rebase-merge settings, with branch auto-deletion off | every commit lands on `main` |
| `ruleset` | the default-branch ruleset | merges blocked until checks pass |
| `security` | Dependabot, CodeQL, and secret scanning | security alerts and updates |

## Profiles

- **Light**: `labels` only. For an existing project whose GitHub setup should stay exactly as
  it is. AStack plans, builds, reviews, and merges using what the repo already has.
- **Custom**: `labels`, plus the items the user picks.
- **Full**: every item. The default for a new repo.

The footprint can grow later: rerun `/astack:setup` and add items.

## Rules for every profile

- **Preview first.** Before changing anything, show a table with each item, what the repo has
  now, and what AStack would do. Apply only what the user approves.
- **Never overwrite.**
  - A label that already exists keeps its colour and description, so labels are created
    without `--force`.
  - An existing file is merged (the `AGENTS.md` block) or left alone.
  - An existing workflow is never edited. When `ci` is managed in a repo that already has CI,
    the slop gate goes in a new `astack-slop.yml` workflow instead.
- **Record what changed.** Every setting `setup` changes is listed with its previous value in
  the setup PR body, or in an issue titled "AStack setup record" when there's no PR, so it can
  be restored.

## When an item isn't managed

| Not managed | How the skills behave |
|---|---|
| `agents-md` | Agents read the repo's own `AGENTS.md` or `CLAUDE.md`. Briefs still carry AStack's rules |
| `ci` | "Checks" means the repo's own required checks, or every check on the PR when none are required. Slop rules are enforced by the deslop pass and review only |
| `merge` | Merge with a method the repo allows: rebase if allowed (`gh api repos/{owner}/{repo} --jq '{allow_rebase_merge,allow_merge_commit,allow_squash_merge}'`), else a merge commit, else squash. Tell the user when squash would collapse the PR's commits |
| `deploy` | Deploy tracking uses the repo's own workflow that deploys on pushes to the default branch, if the scout finds one. Otherwise there's no deploy evidence, and a merge counts as done once checks on the default branch pass. `ship` doesn't run: AStack doesn't manage delivery in this repo |
| `ruleset` | Nothing on GitHub blocks a merge on failing checks, so AStack's own merge gates still require them |
| `security` | Nothing changes for the skills |
