---
name: setup
description: Set up a GitHub repository for AStack once - labels, issue and PR templates, AGENTS.md, CI and deploy workflows, separate development and production environments, branch rules, and security settings. Use when starting a project or adopting AStack in an existing repo.
disable-model-invocation: true
---

# Setup

Installs the GitHub side of AStack in the current repo. Practices and exact commands:
`../../docs/environments.md`. Labels and bodies: `../../docs/github.md`. Routing:
`../../docs/routing.md`. Everything is idempotent: check what exists before creating it.

1. **Confirm the target.** `gh repo view --json nameWithOwner,visibility,viewerPermission` and
   `gh api user --jq .plan.name`. You need admin permission. A `null` plan means the token
   lacks the `read:user` scope: ask the user to run `! gh auth refresh -s read:user`, or
   continue and treat each refusal as a plan gap. Tell the user up front which gates their plan
   can't enforce and the fallback for each. A private repo on the free plan gets no
   environments: offer its three options from `../../docs/environments.md` and let the user
   choose. Record the result as `ASTACK_SECRETS_MODE` (`environments` or `prefixed`), and
   write every later step and file to match it.
2. **Learn the project.** Send a **scout** for: the language, framework, and package manager,
   the existing scripts for format, lint, typecheck, test, and build, existing workflows, and
   the deploy host. A new project gets its stack and host from its spec or map. If the repo
   has no application and no spec or map says, don't ask: the stack is decided in **chart**,
   and the walking-skeleton slice writes the stack-specific files. Otherwise, if nothing says,
   use the **grill** skill on just those questions.
3. **Labels.** Have the **clerk** create every label in `../../docs/github.md` with
   `gh label create <name> --color <hex> --description "<meaning>" --force`.
4. **Files.** A repo with no commits has no `main` for a PR to target. First push one commit
   straight to `main` holding only the `.gitignore`; this is the only direct commit AStack
   ever makes to `main`. Then, on branch `astack-setup`, brief the **builder** agent to write
   the files listed
   under "Files `setup` writes", with the commands from step 2 and the slop gate from
   `../../docs/slop.md` (ask the user before adding a dev dependency the gate needs; an
   existing repo may need a first PR that clears current hits). Each workflow's third-party
   actions must be pinned to a commit SHA the scout looked up. If the repo has no application
   yet, skip `ci.yml`, `deploy.yml`, and the slop gate, and leave `dependabot.yml` at
   `github-actions`; the walking-skeleton slice adds those.
   `AGENTS.md` and `CLAUDE.md` follow `../../docs/agents-md.md`: the scout reports the
   project's conventions with file paths, and the builder writes only the AStack block. Before
   moving any existing `CLAUDE.md` content, ask the user, as the table there says. Verify the YAML parses, push, and open a PR. Merging it is the user's call.
5. **Settings.** After the user agrees, apply merge settings, the `development` and
   `production` environments with production's tag-only deployment policy and required
   reviewer, and the security settings. Report each refusal by plan as a gap, not an error.
6. **Secrets.** List every variable each environment needs, from `.env.example` and the spec.
   Tell the user to set each value themselves with the command for the repo's
   `ASTACK_SECRETS_MODE` (`../../docs/environments.md`), prefixed with `!` to run it in this
   session. Never ask for a secret value in chat.
7. **Branch ruleset.** Once CI has run and the `ci` check exists, create the default-branch
   ruleset. When there's no CI yet, say it waits for the walking skeleton and that the
   **ship** skill re-checks it.
8. **Report** a table: each item applied, skipped as already present, or not available on this
   plan, including the effective branch-retention setting. Then point to the next step: **chart** for a new project, **build** for an existing one.
