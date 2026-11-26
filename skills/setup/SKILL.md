---
name: setup
description: Set up a GitHub repository for AStack - asks how much of the repo's GitHub setup AStack may change, then installs only that. Light adds just the labels, so an existing project keeps its workflows, settings, and rules. Full adds labels, templates, AGENTS.md, CI and deploy workflows, separate development and production environments, branch rules, and security settings. Use when starting a project or adopting AStack in an existing repo.
disable-model-invocation: true
---

# Setup

Installs the GitHub side of AStack in the current repo, within the footprint the user chooses
(`../../docs/footprint.md`). Practices and exact commands: `../../docs/environments.md`.
Labels and bodies: `../../docs/github.md`. Routing: `../../docs/routing.md`.

Everything is idempotent. Each step first compares what it would create with what already
exists on GitHub (labels, files on `main` or the `astack-setup` branch, settings, environments,
variables), then does only what's missing. So a rerun after an interruption resumes where it
stopped, and a rerun can also grow the footprint.

1. **Confirm the target.** `gh repo view --json nameWithOwner,visibility,viewerPermission`.
   The Light profile only needs permission to create labels and variables. Any other item
   needs admin.
2. **Learn the project.** Send a **scout** for:
   - whether the repo has commits and application code
   - the language, framework, and package manager
   - the existing scripts for format, lint, typecheck, test, and build
   - existing workflows, and which one deploys, if any, along with the deploy host
   - existing labels, templates, `AGENTS.md` or `CLAUDE.md`, merge settings, rulesets or
     branch protection, and environments

   A new project gets its stack and host from its spec or map. If the repo has no application
   and no spec or map says, don't ask: the stack is decided in **chart**, and the
   walking-skeleton slice writes the stack-specific files.
3. **Choose the footprint.** Read `ASTACK_MANAGES` if it's already set. Otherwise ask:
   - **Existing project** (the repo has commits): "Should AStack keep your GitHub setup as it
     is and add only its labels (Light), let you pick what it may change (Custom), or set up
     everything (Full)?" Recommend Light, which is the right default for using AStack only to
     build features.
   - **New repo**: recommend Full, and confirm it.

   For Custom, ask about each item in `../../docs/footprint.md`, and show what the repo has
   now for each. Record the answer with `gh variable set ASTACK_MANAGES --body
   <comma-separated items>`.
4. **Preview.** Show one table covering every managed item: what exists now, and what AStack
   will add or change. Apply only what the user approves, following the "Rules for every
   profile" in `../../docs/footprint.md`. Every step below runs only for items in
   `ASTACK_MANAGES`.
5. **Plan and secrets mode** (`deploy`, `ruleset`, `security`). Run
   `gh api user --jq .plan.name`. A `null` plan means the token lacks the `read:user` scope:
   ask the user to run `! gh auth refresh -s read:user`, or continue and treat each refusal as
   a plan gap. Tell the user which gates their plan can't enforce, and the fallback for each. A
   private repo on the free plan gets no environments, so for `deploy`, offer its three
   options from `../../docs/environments.md` and let the user choose. Record the result as
   `ASTACK_SECRETS_MODE` (`environments` or `prefixed`), and write every later step and file
   to match it.
6. **Labels** (always). Have the **clerk** create each label from `../../docs/github.md` that
   doesn't already exist, with `gh label create <name> --color <hex> --description
   "<meaning>"`. Leave existing labels exactly as they are.
7. **Files** (`agents-md`, `templates`, `ci`, `deploy`, and the `dependabot.yml` part of
   `security`).
   - A repo with no commits has no `main` for a PR to target. First push one commit straight
     to `main` holding only the `.gitignore`. This is the only direct commit AStack ever makes
     to `main`.
   - Then, on branch `astack-setup`, brief the **builder** agent to write the managed files
     listed under "Files `setup` writes" in `../../docs/environments.md`. Use the commands
     from step 2 and the slop gate from `../../docs/slop.md`. Ask the user before adding a dev
     dependency the gate needs; an existing repo may need a first PR that clears current
     hits.
   - Never edit an existing workflow. In a repo that already has CI, the slop gate goes in a
     new `astack-slop.yml`.
   - Pin each workflow's third-party actions to a commit SHA the scout looked up.
   - If the repo has no application yet, skip `ci.yml`, `deploy.yml`, and the slop gate, and
     leave `dependabot.yml` at `github-actions`. The walking-skeleton slice adds those.
   - `AGENTS.md` and `CLAUDE.md` follow `../../docs/agents-md.md`: the scout reports the
     project's conventions with file paths, and the builder writes only the AStack block.
     Before moving any existing `CLAUDE.md` content, ask the user, as the table there says.
   - Verify the YAML parses, push, and open a PR whose body records every change, with each
     setting's previous value. Merging it is the user's call.
8. **Settings** (`merge`, `deploy`, `security`). After the user agrees, apply them: the merge
   settings; the `development` and `production` environments, with production's tag-only
   deployment policy and required reviewer; and the security settings. Record each previous
   value in the setup PR body, or, with no PR, in an issue titled "AStack setup record".
   Report each refusal by plan as a gap, not an error.
9. **Secrets** (`deploy`). List every variable each environment needs, from `.env.example`
   and the spec. Tell the user to set each value themselves with the command for the repo's
   `ASTACK_SECRETS_MODE` (`../../docs/environments.md`), prefixed with `!` to run it in this
   session. Never ask for a secret value in chat.
10. **Branch ruleset** (`ruleset`). Once CI has run and the `ci` check exists, create the
    default-branch ruleset. When there's no CI yet, say it waits for the walking skeleton and
    that the **ship** skill re-checks it.
11. **Record the state** in `ASTACK_SETUP`. Other skills treat the repo as set up only when it
    reads `complete`. Labels alone mean an interrupted setup.
    - No files to write (Light, or a Custom footprint without file items): set it to
      `complete` once the labels and variables exist.
    - A setup PR is open: `gh variable set ASTACK_SETUP --body awaiting-merge`. Builds would
      branch from a `main` that lacks the setup files, so the repo isn't ready yet.
    - The setup PR merged, and the expected files are on the default branch
      (`gh api repos/{owner}/{repo}/contents/<path>` for each file written): set it to
      `complete`.
    - The setup PR closed without merging: set nothing, and tell the user to rerun
      `/astack:setup`.
12. **Report** a table: each item, whether it's managed, and for managed items whether it was
    applied, already present, or not available on this plan. Include the effective
    branch-retention setting when `merge` is managed. Then point to the next step: **chart**
    for a new project, **build** for an existing one.
