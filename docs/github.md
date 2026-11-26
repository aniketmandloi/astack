# GitHub contract

All AStack state lives on GitHub. Nothing about plans, specs, or progress is written to local
files. Every skill reads and writes the shapes below with `gh`, so any session in any harness
can pick up where another left off.

## Safety

- Run `gh repo view --json nameWithOwner,viewerPermission` before the first write of a session.
  In a fork `gh` can default to the upstream; confirm with the user when the repo is not theirs.
- Refer to issues by title (with the link inside it), never by a bare `#number` wall.
- Every issue, comment, PR body, and commit message follows the prose rules in
  `docs/slop.md`.
- Never merge a PR, delete a branch, or approve a production deployment without the user's
  explicit go-ahead in this session. Typing `/astack:mode` is that go-ahead for merges that
  pass its gates (`docs/autonomy.md`), and for nothing else.

## Labels

| Label | Meaning |
|---|---|
| `astack:map` | A chart map: index of decisions for a large effort |
| `astack:decision` | A decision ticket under a map |
| `decision:research` / `decision:prototype` / `decision:grilling` / `decision:task` | Decision ticket type |
| `astack:spec` | A settled spec, ready to slice |
| `astack:slice` | A vertical slice of a spec: buildable work |
| `astack:bug` | A bug report |
| `astack:release` | User work needed only before a production release, such as Connect production or buying the domain. Development runs don't wait on it; `ship` does |
| `astack:retro` | A retro of finished work; its guards are slice sub-issues |
| `astack:run` | An astack mode run's tracking issue (`docs/autonomy.md`) |
| `astack:launch` | A slice needed before the first customer (`docs/launch.md`); added alongside `astack:slice` |
| `status:ready` | Buildable now, pending only its blockers |
| `status:in-progress` | Claimed (the assignee is the claim) |
| `status:in-review` | A PR is open for it |
| `tier:hard` / `tier:small` | Routes to the builder or tweaker agent (`docs/routing.md`) |

Closed means done. Blocked means an open native blocked-by edge; there is no blocked label.

## Issue bodies

**Map** (`astack:map`):

```markdown
## Destination
<what reaching the end looks like: usually "a spec ready to slice". One or two lines.>

## Notes
<domain, standing preferences, skills every session should consult>

## Decisions so far
- [<closed ticket title>](<url>): <one-line gist>

## Not yet specified
<in-scope fog that can't be phrased as a sharp question yet>

## Out of scope
- [<closed ticket title>](<url>): <gist and why it's out>
```

**Decision** (`astack:decision` + `decision:<type>`, sub-issue of its map):

```markdown
## Question
<the decision or investigation this ticket resolves, sized to one session>
```

The answer is recorded as a resolution comment, never edited into the body.

**Spec** (`astack:spec`):

```markdown
## Problem
## Users and outcome
## Scope
### In
### Out
## Decisions
<links to the decision tickets or grill outcome this rests on>
## Behaviour
<user-visible behaviour, as testable statements>
## Technical approach
<modules, data model, interfaces, third-party services>
## Environments
<new config and secrets per environment, migrations, rollout and rollback notes>
## Launch
<new customer-facing projects: each docs/launch.md item, its decision (or "out of scope:
reason"), and its work, split into build work and user work>
## Risks
## Open questions
<must be empty before slicing>
```

**Slice** (`astack:slice` + `status:ready` + `tier:*`, sub-issue of its spec):

```markdown
Part of <spec title and link>
Plan item: S<n>

## What to build
<one vertical slice: thin, end to end through every layer it touches, demoable>

## Acceptance criteria
- [ ] <testable statement>

## Notes
<likely files or modules, test plan, environment impact>
```

**Bug** (`astack:bug`):

```markdown
## What happens
## What should happen
## Steps to reproduce
## Environment
<development or production, version or commit, logs>
```

## Operations

`gh` infers the repo inside a clone. `<db-id>` is an issue's database id:
`gh api repos/{owner}/{repo}/issues/<n> --jq .id`, not its `#number` or `node_id`.
The `gh api` forms below work on every `gh` version; `gh` 2.94+ also has `--parent`,
`--add-sub-issue`, `--blocked-by`, and `--add-blocked-by` flags on `gh issue create/edit`.

- **Create**: `gh issue create --title "<title>" --label "<a>,<b>" --body-file - <<'EOF' ... EOF`
- **Read**: `gh issue view <n> --json number,title,body,labels,assignees,state,comments`
- **List**: `gh issue list --state open --label <label> --json number,title,labels,assignees`
- **Sub-issue**: `gh api -X POST repos/{owner}/{repo}/issues/<parent>/sub_issues -F sub_issue_id=<child-db-id>`
- **List sub-issues**: `gh api repos/{owner}/{repo}/issues/<parent>/sub_issues --jq '.[] | {number,title,state}'`
- **Blocked by**: `gh api -X POST repos/{owner}/{repo}/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`
- **Open blockers**: `gh api repos/{owner}/{repo}/issues/<n> --jq .issue_dependencies_summary.blocked_by` (0 = startable)
- **Claim**: `gh issue edit <n> --add-assignee @me --add-label status:in-progress --remove-label status:ready`
- **Comment**: `gh issue comment <n> --body-file - <<'EOF' ... EOF`
- **Close**: comment first, then `gh issue close <n>` (`--comment` on an already-closed issue is dropped silently)

Create issues first, then wire sub-issue links and blocked-by edges in a second pass: issues
need ids before they can reference each other, and a placeholder `#<n>` links to an unrelated
issue.

**Frontier**: the open sub-issues of a map or spec with no open blocker and no assignee, in
creation order. For buildable work across the repo: open `status:ready` issues with no open
blocker and no assignee, oldest first.

## Branches and pull requests

- One branch per issue from the latest `main`: `<n>-<short-slug>`.
- The PR body starts with `Closes #<n>`, then a `## Why` section stating the goal in one
  sentence (what the change gives its user), then: what changed, how each acceptance criterion
  is met, checks run with results, a Deslop section (the number of rounds, and each finding
  by slop rule number), environment impact, and what the user must check by hand.
  Every claim is labelled measured (run and seen), inferred, or a guess.
- When the PR opens, move the issue to `status:in-review`. Merge is squash-only and needs the
  user's go-ahead.

## Commits, verdicts, and deploys

Every verdict and check belongs to one exact commit.

- **Review**: the review comment opens with `Reviewed at <head-sha>`, from
  `gh pr view <pr> --json headRefOid --jq .headRefOid`. The verdict covers only that commit.
  Any later push needs a review of the new commits before the PR is merge-ready again.
- **Merge**: `gh pr merge <pr> --squash --match-head-commit <reviewed-sha>`. GitHub refuses it
  if the head moved since the review.
- **Deploy**: after merging, take the merge commit
  (`gh pr view <pr> --json mergeCommit --jq .mergeCommit.oid`). Find its own deploy run
  (`gh run list --workflow deploy.yml --commit <merge-sha> --json databaseId,status,conclusion`)
  and watch that run (`gh run watch <id>`). The latest run on `main` may belong to another merge.
- Throwaway prototype branches are `prototype/<n>-<slug>`: pushed, linked from their ticket,
  never merged.
