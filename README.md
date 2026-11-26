# AStack

A GitHub-only workflow for building any project with coding agents, in Claude Code and Codex.
Plans, decisions, specs, work items, reviews, and releases all live in GitHub issues, PRs, and
Environments, so any session in either agent picks up exactly where the last one stopped.
Nothing is written to local planning files.

## The flow

```
            ┌───────── big or foggy ─────────┐
idea ──▶ chart ──▶ (decision tickets) ──▶ spec ──▶ slice ──▶ build ──▶ review ──▶ merge
   └──▶ grill ─────────────────────────────▲                ▲                      │
   └──▶ small, clear change ────────────────┼──────────▶ build                     ▼
   └──▶ bug ──▶ fix ────────────────────────┘                       main ──▶ development
                                                            ship ──▶ release ──▶ production
```

Start anywhere with **`/astack:astack`** (Codex: `$astack`). It reads the repo's GitHub state
and routes to the right step. Or hand over the whole thing with **`/astack:mode <goal>`**,
which runs every step itself under the rules in [docs/autonomy.md](docs/autonomy.md).

| Skill | Does |
|---|---|
| `astack` | Entry point: orients from GitHub and routes any request |
| `help` | Read-only guide: answers any question about AStack from its own files, and says what to do next in this repo |
| `chart` | Maps a large effort (a new project, a big feature) as decision tickets, one per session |
| `grill` | Interviews you until every decision in a one-session plan is settled |
| `spec` | Writes settled decisions up as an `astack:spec` issue |
| `slice` | Splits a spec into vertical-slice sub-issues with acceptance criteria and a tier |
| `build` | Takes one issue to a tested PR through the right-tier agent |
| `fix` | Takes a bug to a reproducing test, a root-cause fix, and a PR |
| `review` | Reviews a PR against its issue in a fresh context and posts the findings |
| `babysit` | Keeps a PR merge-ready: CI failures, merge conflicts, review comments. Never merges |
| `triage` | Sorts unlabelled issues and customer feedback into bugs, slices, and plans |
| `retro` | Turns mistakes that repeated across a finished spec into guards: types, lint rules, tests, pitfalls |
| `setup` | One-time repo setup: labels, templates, CI/CD, dev and prod environments, rules *(you start it)* |
| `ship` | Cuts a release and watches the gated production deploy *(you start it)* |
| `mode` | Autonomous: drives a goal through every stage to development on its own, records each decision on GitHub, and pauses only for production, money, secrets, destructive actions, and your calls *(you start it)* |

## Model routing

Skills orchestrate; four agents do the work, each pinned to a model and effort
([docs/routing.md](docs/routing.md)):

| Agent | Work | Claude Code | Codex |
|---|---|---|---|
| builder | Difficult code, debugging, reviews | Opus 5.5, high | gpt-6.2-sol, high |
| tweaker | Small contained edits | Opus 5.5, medium | gpt-6.2-sol, high |
| scout | Search, `gh` reads, docs lookups | Haiku 5.5, high | gpt-6.2-sol, low |
| clerk | Bulk, fully specified `gh` writes | Haiku 5.5, high | gpt-6.2-sol, low |

## Guard

In Claude Code, a PreToolUse hook (`hooks/guard.py`) checks every Bash command the agent runs
and denies these:
- `git push` with `--force`, `-f`, or a `+` refspec; `--force-with-lease` to `main`
- deleting a branch, locally (`git branch -d/-D/--delete`) or on the remote
- `rm -rf` on a path outside the working directory, or on the directory itself
- `gh repo delete`, `gh release delete`, `gh issue delete`, and `gh api` DELETE requests
- `DROP TABLE/DATABASE/SCHEMA` or `TRUNCATE` in a command that runs a SQL client
  (`psql`, `mysql`, `sqlite3`, and similar)

It only sees shell commands. It can't see GitHub settings, an ORM's own CLI, or anything done
outside the agent. Run a blocked command yourself with `! <command>` if you mean it. Tests:
`python3 -m unittest hooks/test_guard.py`.

## Install

**Claude Code**

```
/plugin marketplace add aniketmandloi/astack
/plugin install astack@astack
```

**Codex**

```bash
codex plugin marketplace add aniketmandloi/astack
mkdir -p ~/.codex/agents && cp codex/agents/*.toml ~/.codex/agents/
```

Then install AStack from `/plugins` inside Codex and start a new session. Codex plugins don't
carry custom agents, so the second command installs the four routing agents from a clone of
this repo.

Both need the [GitHub CLI](https://cli.github.com/) signed in (`gh auth login`).

## Docs

- [docs/github.md](docs/github.md): labels, issue bodies, `gh` operations, branch and PR rules
- [docs/environments.md](docs/environments.md): development vs production, CI/CD, secrets,
  repo settings, releases
- [docs/app-checks.md](docs/app-checks.md): end-to-end and smoke tests in CI, and hands-on
  checks that the agent runs or writes up for you (`ASTACK_APP_CHECKS`)
- [docs/launch.md](docs/launch.md): launch readiness that `chart` plans for every new
  customer-facing project, and `ship` checks before the first customer release
- [docs/agents-md.md](docs/agents-md.md): the rules block `setup` writes into each project's
  `AGENTS.md` (imported by `CLAUDE.md`), so plain sessions follow the same practices
- [docs/routing.md](docs/routing.md): which agent and model handles what
- [docs/slop.md](docs/slop.md): what never ships, and what stops it: agent briefs, a
  fresh-context deslop pass before every PR, `review`, and a CI gate that blocks the merge

## Credits

`grill` and `chart` adapt Matt Pocock's `grilling` and `wayfinder` skills (MIT). See
[CREDITS.md](CREDITS.md).
