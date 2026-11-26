# Model routing

AStack skills are orchestrators: they talk to the user, decide, and read GitHub. They hand
every piece of real work to one of four agents, and each agent pins its own model and effort.
The routing lives in the agents, not the skills, because in Claude Code a skill's `model` only
applies when the user types `/name`; an agent's `model` and `effort` apply every time it runs.

| Agent | Work | Claude Code | Codex |
|---|---|---|---|
| **builder** | Difficult code: features, multi-file changes, architecture, migrations, security, root-cause debugging, reviews | `astack:builder`: `claude-opus-5-5`, effort `high` | `astack_builder`: `gpt-6.2-sol`, `high` |
| **tweaker** | Small contained edits: copy, style, small UI, renames, config bumps | `astack:tweaker`: `claude-sonnet-5-5`, effort `high` | `astack_tweaker`: `gpt-6.2-sol`, `high` |
| **scout** | Read-only fact finding: code search, `gh` reads, docs, versions | `astack:scout`: `claude-haiku-5-5`, effort `high` | `astack_scout`: `gpt-6.2-sol`, `high` |
| **clerk** | Mechanical, fully specified `gh` writes in bulk | `astack:clerk`: `claude-haiku-5-5`, effort `high` | `astack_clerk`: `gpt-6.2-sol`, `high` |

To change a tier, edit one line in `agents/<name>.md` (Claude Code) or
`codex/agents/astack_<name>.toml` (Codex), and keep the pair's instructions in sync.

## How to delegate

- **Claude Code**: call the Agent tool with `subagent_type` set to the agent's name above.
- **Codex**: spawn the custom agent by its name above.

A brief is self-contained: the agent sees none of the conversation. Include the issue number
and body, its acceptance criteria, the branch, the facts already found, and what to return.
For the builder and tweaker, include the full text of `docs/slop.md`. For the clerk, include
the exact `gh` commands from `docs/github.md` it should use.

## Choosing the agent

- An issue labelled `tier:hard` goes to the **builder**; `tier:small` goes to the **tweaker**.
  Unlabelled: builder when in doubt. A tweaker that reports "bigger than it looked" hands off
  to the builder with its findings.
- Anything that needs facts you do not have: **scout**. Run independent scouts in parallel.
- Three or more GitHub writes whose content is already decided: **clerk**. One or two: do them
  yourself; a delegation costs more than the call.
- Talking with the user, making decisions, and writing specs stay in the orchestrating session.

## Caveats

- `effort` overrides the session's effort level but not the `CLAUDE_CODE_EFFORT_LEVEL`
  environment variable; `xhigh` and `max` are Opus-only.
- Setting `CLAUDE_CODE_SUBAGENT_MODEL` with `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` overrides
  every agent's `model`, which defeats this routing.
- Codex plugins do not ship custom agents, so the Codex agents are installed by copying
  `codex/agents/*.toml` to `~/.codex/agents/` (see the README).
