# AGENTS.md

`setup` writes the project's standing rules into `AGENTS.md`, which Codex reads, and points
`CLAUDE.md` at it with an `@AGENTS.md` import, which Claude Code follows. A plain session in
either agent then follows the same practices as an AStack skill does.

## The AStack block

AStack owns only the text between `<!-- astack:start -->` and `<!-- astack:end -->`. Re-running
`setup` replaces that block and nothing else. Everything outside it belongs to the user.

- Fill every value from the repo. Omit a command line the project doesn't have; on a repo
  with no application yet, the Commands section is the single line "None yet: the
  walking-skeleton slice adds them."
- Conventions come only from evidence in the code (the scout reports them with file paths).
  Leave the section out rather than invent conventions.
- Keep the block under 70 lines. The code rules restate `docs/slop.md` one line each; keep the
  two in sync.
- Pitfalls come only from `retro`: each one is a mistake agents made here more than once that
  no stronger guard could prevent. Leave the section out until there is one.

## Existing files

| Repo has | `setup` does |
|---|---|
| No `AGENTS.md` | Creates it with the block |
| `AGENTS.md` without the block | Appends the block at the end |
| `AGENTS.md` with the block | Replaces the block only |
| No `CLAUDE.md` | Creates it containing `@AGENTS.md` |
| `CLAUDE.md` with content | Asks the user whether to move that content into `AGENTS.md` above the block, leaving `CLAUDE.md` as `@AGENTS.md`. If they decline, it adds `@AGENTS.md` as the first line and changes nothing else |
| `CLAUDE.md` already importing `@AGENTS.md` | Leaves it alone |

## Template

```markdown
<!-- astack:start -->
## AStack

This repo uses the AStack workflow: plans, specs, and work items live in GitHub issues.

### Commands

- Install: `<command>`
- Dev server: `<command>` (the user starts it; agents never do)
- Test: `<command>`
- Lint and format: `<command>`
- Typecheck: `<command>`
- Build: `<command>`

### Workflow

- Every change starts from a GitHub issue. One branch per issue, `<n>-<slug>`, from an
  up-to-date `main`.
- Never commit to or push `main`. PRs start with `Closes #<n>` and squash-merge after CI passes.
- Commit each verified logical step separately.
- Deferred work becomes a GitHub issue, never a TODO.

### Environments

- Every merge to `main` deploys to `development`; only a GitHub release deploys to `production`.
- All config comes from environment variables. Nothing in code differs between environments.
- Every new variable goes in `.env.example` with a safe dummy value. Never commit a secret or
  a real `.env` file.
- Database changes go only through versioned migrations that are safe to run while the
  previous release still serves traffic.

### Code rules

None of these ship:

1. Dead code, including code this change made unused.
2. Commented-out code.
3. Debug output or leftover logging.
4. TODO, FIXME, HACK, stubs, or fake data outside tests.
5. Options, layers, or abstractions nobody asked for.
6. A helper, type, or dependency that duplicates an existing one.
7. Checks for impossible states, or try/catch that swallows errors.
8. `any`, unchecked casts, or lint and type suppressions used to pass a check.
9. Comments that restate the code; comments say only what the code cannot.
10. Tests that assert nothing or pass without the change.
11. Reformatting or refactors outside the issue.
12. Style that differs from the surrounding code.
13. Vague names (`data`, `util`, `helper`, `temp`) where a domain name exists.

### Conventions

- <convention found in the code, with an example path>

### Pitfalls

- <a mistake agents have repeated here, and what to do instead>
<!-- astack:end -->
```
