# AStack

My stack for building software with coding agents. I use it every day in Claude Code and
Codex to start projects, add features, change UI, fix bugs, and ship to production. It keeps
every plan, decision, task, review, and release on GitHub, so any session in either agent picks
up exactly where the last one stopped.

## Why I built it

I've worked with most of the popular agent workflows: the BMAD Method, gstack, pstack, and
Matt Pocock's skills. Each one taught me something, and each one had a part that slowed me
down.

- **BMAD** got me thinking in phases (analysis, PRD, architecture, stories, dev, QA). But it
  writes a lot of planning documents to disk and runs a lot of ceremony around them.
- **gstack** showed me how useful role-based reviews and an opinionated ship flow are. But it
  is built around one person's setup.
- **pstack** (poteto-mode) is the most rigorous of them: deslop, evidence for every claim,
  subagents with fresh context, and the right model per role. It's also large, Cursor-first,
  and keeps its state in the local session.
- **Matt Pocock's skills** are sharp, and his `grill-me` and `wayfinder` changed how I plan.
  They're individual skills, though, not a path from idea to production.

What I wanted was one small stack that does the whole job and follows one rule: **all state
lives on GitHub.** There are no planning files on my laptop. Issues hold the plans, PRs hold
the work, and GitHub Environments hold development and production. So I took the practices
that worked for me from each of them and built AStack around that rule.

## What I took from each

| From | What I kept |
|---|---|
| Matt Pocock's skills | Grilling a plan until every decision is settled (`grill`). Charting big, foggy work as decision tickets on the issue tracker (`chart`, adapted from `wayfinder`). Triage, and retros |
| BMAD | Clear phases: plan, spec, slice, build, review. An `AGENTS.md` block of project rules with a pitfalls section. Reading earlier architecture decisions before a new spec. End-to-end tests for every user-facing feature |
| gstack | Reviews in a fresh context, a gated ship flow, a guard against destructive commands, and docs kept in step with releases |
| pstack | No slop in code or prose. Every claim labelled measured, inferred, or guess. Naming the data shape before writing code. Prototyping instead of asking when an experiment can answer. Babysitting PRs to green, and checking what a change could break beyond the diff |

## What it does for me

- **I can stop and resume anywhere.** Because state lives in issues and PRs, I can switch
  machines, start a new session, or move from Claude Code to Codex, and the next session reads
  GitHub and carries on. `/astack:help` tells me where I am and what to do next.
- **Each task gets the right model.** Hard code goes to Opus at high effort, small edits to
  Opus at medium, and searching and GitHub chores to Haiku. I don't pick a model per task.
- **No slop ships.** One list of slop rules covers code and prose. The agent writing the code
  gets the list in its brief, a fresh agent checks the diff against it before the PR opens
  and again in review, and a CI check blocks the merge on the rules a linter can catch.
- **Development and production are separate from day one.** Each has its own environment,
  secrets, and data. Merging to `main` deploys to development. Only a release I create reaches
  production, and I can roll back to the previous release.
- **It plans the launch, not just the code.** For a new product, the plan includes the domain,
  payments, terms and privacy, backups, alerts, support, and the one metric that shows a
  customer got value.
- **It gets better over time.** When a spec is done, `retro` finds mistakes that repeated and
  turns each into a lint rule, a test, a type, or a pitfall in `AGENTS.md`, so it can't
  happen again.
- **It can run on its own.** `/astack:mode` takes a goal and drives it all the way to
  development. It records every decision on GitHub for me to override, and it stops before
  anything only I should do.

## Install

You need the [GitHub CLI](https://cli.github.com/) signed in (`gh auth login`).

**Claude Code**

```
/plugin marketplace add aniketmandloi/astack
/plugin install astack@astack
```

**Codex**

```bash
codex plugin marketplace add aniketmandloi/astack
git clone https://github.com/aniketmandloi/astack
mkdir -p ~/.codex/agents && cp astack/codex/agents/*.toml ~/.codex/agents/
```

Then install AStack from `/plugins` inside Codex, and start a new session. Codex plugins don't
carry custom agents, so the copy step installs the five model-routing agents.

## How I use it

### Once per repo

```
gh repo create my-app --private --clone && cd my-app
/astack:setup
```

Setup first asks how much of my GitHub setup AStack may change, then shows me a preview of
every change before it applies anything:

- **Light**: only AStack's labels. Workflows, settings, rules, and files stay exactly as they
  are. This is what I pick on a project that's already built, where I only want AStack for
  features.
- **Custom**: I pick the pieces: the `AGENTS.md` rules, templates, CI with the slop gate,
  deploy with dev and prod environments, rebase merges, branch rules, and security.
- **Full**: everything. This is what I pick for a new repo.

It never re-colours a label I already have and never edits an existing workflow. It also
records the previous value of every setting it changes, so I can put it back. I can rerun it
later to add more. Whatever I leave to the repo, the other skills work with what's already
there: its own checks, its merge method, and its deploy workflow
([docs/footprint.md](docs/footprint.md)).

### Starting a new project

```
/astack:chart "my idea..."
```

The first session asks about where I'm heading and the whole problem space: who it's for,
scope, stack, hosting, what artifact reaches a user and how we verify it, look and feel,
launch readiness, and the riskiest assumption. It creates a map issue of decision tickets.
Research tickets are answered by a scout on their own. After that, each session works through
one ticket with me, by asking questions or showing a throwaway prototype.

When the map is clear:

```
/astack:spec <map>      writes the decisions up as a spec issue I correct
/astack:slice <spec>    splits it into issues I approve
```

The first slices are always the same three:
1. **Connect development**: my task, setting up hosting and secrets.
2. **The walking skeleton**: the thinnest version of the app that reaches development, with
   CI, a deploy workflow, a smoke test, and a health check.
3. **Connect production**: my task again, which can wait until I'm ready to release.

### Building

```
/astack:build           picks the next ready slice, then does everything up to merge-ready
```

That one command runs the whole loop:
1. The right-tier agent builds the slice test-first, and it gets verified and deslopped.
2. A fresh agent reviews the branch before anything is pushed. Fixes get a delta review that
   covers only the new commits, not the whole PR again.
3. Once the review is clean, the `pr` skill opens one PR. Its description has a summary, a
   table of changed files, a Mermaid diagram of the flow, each acceptance criterion with its
   evidence, the review result, and a risk rating with the blast radius. CI runs once, on
   reviewed code.
4. Babysit keeps the PR green and answers comments.

Then I merge, and it deploys to development. Merges are rebase merges, so every commit lands on
`main`.

For a clear feature, a UI change, or a small tweak, I skip planning and go straight to
`/astack:build "what I want"`. It files the issue first. When a feature still has open
decisions, I start with `/astack:grill`.

### Reviewing in the other agent

When I build in Claude Code, I can have Codex review it, or the other way round. Before the
branch review, it asks once per issue: "Review here, or in another CLI?" If I choose another
CLI, it writes the brief inside `.git` and gives me one line to paste into Codex:
`Read <path> and follow it.` I paste Codex's reply back, and the agent checks that it covers
the current commit before it fixes anything. Delta rounds work the same way, best in the same
Codex session. The result names its reviewer (`Reviewed at <sha> by codex`), so later
re-reviews on the PR use the same one without asking. In `/astack:mode`, I pick the reviewer
once when the run starts ("..., review with codex"). Each review then waits under "Waiting
on you" while the run works on other slices.

### Fixing and cleaning up

```
/astack:fix "what's broken"     a failing test first, then a root-cause fix
/astack:build                   on a refactor issue: behaviour stays the same, proven by tests
```

### Letting it run

```
/astack:mode "add team invites to the dashboard"
/astack:mode "a habit tracker for students" plan only
```

Mode creates a run issue and works only inside the goal's scope. It plans, builds, reviews,
and merges into development. Every decision it makes is posted on GitHub for me to override.
It never releases to production, spends money, sets secrets, deletes anything, messages
customers, or makes calls that are mine, like pricing, legal, naming, or who the first customer
is. Those go on a "Waiting on you" list while it keeps working on everything else. Running
`/astack:mode` with no goal resumes the open run.

### Releasing

```
/astack:ship
```

Ship checks that CI is green, the development deploy succeeded, production secrets are set,
and launch items are done. It proposes a version, cuts the release once I say yes, and watches
the production deploy. If the deploy fails, it offers to roll back to the previous release.

### After launch

```
/astack:triage      sorts new issues and customer feedback into bugs, slices, and plans
/astack:retro       turns mistakes that repeated into permanent guards
```

### When I'm lost

```
/astack:help                    where am I, what's waiting on me, what to run next
/astack:help how does deslop work?
/astack:astack "anything"       routes the request to the right skill and starts it
```

## Skills

| Skill | What it does |
|---|---|
| `astack` | Entry point: reads the repo's GitHub state and routes any request |
| `help` | Read-only: answers questions about AStack from its own files and says what to do next |
| `chart` | Maps a large effort as decision tickets on GitHub, one ticket per session |
| `grill` | Interviews me until every decision in a one-session plan is settled |
| `spec` | Writes settled decisions up as a spec issue |
| `slice` | Splits a spec into vertical-slice issues with acceptance criteria and a tier |
| `build` | Takes one issue to a tested PR through the right-tier agent |
| `fix` | A reproducing test, a root-cause fix, and a PR |
| `review` | A fresh-context review against the issue, before the PR opens, here or in the other agent; re-reviews cover only new commits |
| `pr` | Opens the PR with a summary, file table, Mermaid diagram, evidence, review result, and risk |
| `babysit` | Keeps a PR merge-ready: CI, conflicts, review comments. Never merges |
| `triage` | Sorts unlabelled issues and feedback |
| `retro` | Turns repeated mistakes into guards |
| `setup` | One-time repo setup *(only I start it)* |
| `ship` | Releases to production *(only I start it)* |
| `mode` | Runs a goal end to end on its own *(only I start it)* |

## Model routing

Skills decide and talk to me; five agents do the work. Each agent has its model and effort
pinned, because in Claude Code a skill's own `model` setting only applies when I type its
slash command ([docs/routing.md](docs/routing.md)).

| Agent | Work | Claude Code | Codex |
|---|---|---|---|
| builder | Hard code, debugging, refactors, reviews | Opus 5.5, high | gpt-6.2-sol, high |
| tweaker | Small contained edits | Opus 5.5, medium | gpt-6.2-sol, high |
| scout | Search, GitHub reads, docs lookups | Haiku 5.5, high | gpt-6.2-sol, low |
| clerk | Bulk, fully specified GitHub writes | Haiku 5.5, high | gpt-6.2-sol, low |
| writer | PR descriptions, from the builder's report and diagram sketch | Haiku 5.5, high | gpt-6.2-sol, medium |

## Testing the running app

End-to-end tests and smoke tests run in CI, on GitHub's machines, so they cost my laptop
nothing. Hands-on checks, where someone actually uses the app, are different, because an agent
needs local browser automation and plenty of memory for them. The first time one is needed,
AStack asks me whether it should run them or write them up for me as a checklist on the issue.
It saves my answer as the repo variable `ASTACK_APP_CHECKS`. On my 8 GB machine I choose the
checklist ([docs/app-checks.md](docs/app-checks.md)).

## Guard

In Claude Code, a hook (`hooks/guard.py`) checks every shell command an agent runs and denies
these:
- `git push` with `--force`, `-f`, or a `+` refspec, and `--force-with-lease` to `main`
- deleting a branch, locally (`git branch -d/-D/--delete`) or on the remote
- `rm -rf` on a path outside the working directory, or on the directory itself
- `gh repo delete`, `gh release delete`, `gh issue delete`, and `gh api` DELETE requests
- `DROP TABLE/DATABASE/SCHEMA` or `TRUNCATE` in a command that runs a SQL client
  (`psql`, `mysql`, `sqlite3`, and similar)

It only sees shell commands, not GitHub settings or an ORM's own CLI. If I really mean one of
these, I run it myself with `! <command>`. Tests: `python3 -m unittest hooks/test_guard.py`.

## What AStack keeps on GitHub

- **Labels**: `astack:map`, `astack:decision`, `astack:spec`, `astack:slice`, `astack:bug`,
  `astack:launch`, `astack:release`, `astack:retro`, `astack:run`, plus `status:*`, `tier:*`,
  and `decision:*` ([docs/github.md](docs/github.md)).
- **Repo variables**: `ASTACK_SETUP` (whether setup finished), `ASTACK_MANAGES` (which parts
  of the GitHub setup AStack may change), `ASTACK_SECRETS_MODE` (how deploy secrets are
  stored), and `ASTACK_APP_CHECKS` (who runs hands-on checks).
- **Everything else**: issue bodies, comments, and PRs.

## Docs

- [docs/footprint.md](docs/footprint.md): what setup may change (Light, Custom, Full), and how
  the skills work with a repo's own setup
- [docs/github.md](docs/github.md): labels, issue bodies, `gh` operations, branches, PRs,
  merges, and deploy tracking
- [docs/environments.md](docs/environments.md): development vs production, artifact kinds,
  CI/CD, secrets, repo settings, releases, and rollback
- [docs/slop.md](docs/slop.md): what never ships, in code and in prose
- [docs/app-checks.md](docs/app-checks.md): CI tests and hands-on checks
- [docs/launch.md](docs/launch.md): launch readiness for a new product
- [docs/autonomy.md](docs/autonomy.md): what `mode` decides and when it stops for me
- [docs/agents-md.md](docs/agents-md.md): the rules block `setup` writes into each project
- [docs/routing.md](docs/routing.md): which agent and model does what

## Credits

`grill` and `chart` adapt Matt Pocock's `grilling` and `wayfinder` skills, and the prose rules
in `docs/slop.md` condense pstack's `unslop` skill. Both are MIT-licensed; see
[CREDITS.md](CREDITS.md). Ideas, but not text, also came from the BMAD Method and gstack.
