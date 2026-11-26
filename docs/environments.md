# Environments and delivery

The practices `setup` installs and `ship` relies on. Development and production are separate
environments with separate config, secrets, and data; code moves from one to the other only
through `main` and a release.

## Flow

```
issue branch ──PR + CI──▶ main ──push──▶ deploy: development (automatic)
                                 └─release vX.Y.Z──▶ deploy: production (gated)
```

- Trunk-based: `main` is always deployable; short-lived branch per issue; squash merge.
- Every merge to `main` deploys to **development**. A published GitHub release deploys that tag
  to **production**. A manual run of the deploy workflow with an older tag is the rollback.
- PR previews, when the host offers them, deploy with development config and never touch
  production data.

## Config and secrets

- Twelve-factor: all config comes from environment variables. Nothing in code differs between
  environments.
- Commit `.env.example` with every variable name and a safe dummy value; gitignore `.env*`
  except that file.
- Deploy-time secrets are GitHub **environment secrets** (`gh secret set <NAME> --env
  development|production`), never repository secrets, so a development job cannot read a
  production secret.
- Each environment has its own resources: database, storage buckets, API keys, OAuth apps,
  webhooks. Never copy production data into development.
- Prefer OIDC federation to the cloud host over long-lived deploy keys where the host supports it.

## Repository settings (via `gh api`)

Check what the plan allows first: `gh repo view --json visibility` and
`gh api user --jq .plan.name`. On a private repo, rulesets, environments, and environment
secrets need GitHub Pro, Team, or Enterprise, and required reviewers on an environment need
Enterprise. When a gate isn't available, say so and use the fallback listed.

**Merge settings**:
```bash
gh api -X PATCH repos/{owner}/{repo} -F allow_squash_merge=true -F allow_merge_commit=false \
  -F allow_rebase_merge=false -F delete_branch_on_merge=true
```

**Environments**:
```bash
gh api -X PUT repos/{owner}/{repo}/environments/development
gh api -X PUT repos/{owner}/{repo}/environments/production --input - <<'EOF'
{"reviewers":[{"type":"User","id":<user-id>}],
 "deployment_branch_policy":{"protected_branches":false,"custom_branch_policies":true}}
EOF
gh api -X POST repos/{owner}/{repo}/environments/production/deployment-branch-policies \
  -f name='v*' -f type=tag
```
`<user-id>` is `gh api user --jq .id`. Without required reviewers, the fallback gate is that
production deploys only from a release, and only `ship` (user-invoked) creates releases.

**Ruleset on the default branch** (create after the CI workflow has run once, so the `ci`
check exists):
```bash
gh api -X POST repos/{owner}/{repo}/rulesets --input - <<'EOF'
{"name":"main","target":"branch","enforcement":"active",
 "conditions":{"ref_name":{"include":["~DEFAULT_BRANCH"],"exclude":[]}},
 "rules":[{"type":"deletion"},{"type":"non_fast_forward"},{"type":"required_linear_history"},
  {"type":"pull_request","parameters":{"required_approving_review_count":0,
   "dismiss_stale_reviews_on_push":true,"require_code_owner_review":false,
   "require_last_push_approval":false,"required_review_thread_resolution":true}},
  {"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":true,
   "required_status_checks":[{"context":"ci"}]}}]}
EOF
```
`required_approving_review_count` is 0 because a solo author cannot approve their own PR;
raise it when the repo has more than one maintainer. No ruleset available: say so; the
workflow still runs CI on every PR.

**Security**:
```bash
gh api -X PUT repos/{owner}/{repo}/vulnerability-alerts          # Dependabot alerts
gh api -X PUT repos/{owner}/{repo}/automated-security-fixes      # Dependabot security PRs
gh api -X PATCH repos/{owner}/{repo} --input - <<'EOF'
{"security_and_analysis":{"secret_scanning":{"status":"enabled"},
 "secret_scanning_push_protection":{"status":"enabled"}}}
EOF
gh api -X PATCH repos/{owner}/{repo}/code-scanning/default-setup -f state=configured  # CodeQL
```
Secret scanning and CodeQL on private repos need GitHub's paid security products; report a
refusal rather than retrying.

## Files `setup` writes

- `.github/workflows/ci.yml`: on `pull_request` and push to `main`. One job with id `ci`:
  install from the lockfile, format check, lint, typecheck, test, build. Commands come from
  the project's own scripts.
- `.github/workflows/deploy.yml`:
  - triggers: push to `main` → `development`; `release: published` → `production`;
    `workflow_dispatch` with a `ref` input → `production` (rollback to that tag).
  - each deploy job sets `environment:` so it gets that environment's secrets and gates, and
    `concurrency: deploy-<environment>` with `cancel-in-progress: false`.
  - the deploy step uses the host's official CLI or action. After deploying it checks the
    health endpoint and fails the job if that check fails.
- Every workflow: top-level `permissions: contents: read`, raised per job only where needed
  (`id-token: write` for OIDC, `deployments: write`). Third-party actions are pinned to a full
  commit SHA with the version in a trailing comment.
- `.github/dependabot.yml`: weekly updates for the project's package ecosystem and for
  `github-actions`.
- `.github/ISSUE_TEMPLATE/bug.yml` and `spec.yml` matching the bodies in `docs/github.md`, and
  `.github/pull_request_template.md` matching its PR body.
- `.env.example`, `.gitignore` entries for `.env*`, and `AGENTS.md` with the project's
  commands, conventions, and a pointer to this workflow. `CLAUDE.md` contains just `@AGENTS.md`.

## Application baseline (built by the walking-skeleton slice)

- A health endpoint (or the host's equivalent) that the deploy job checks.
- Structured logs, and error tracking tagged with the environment name.
- Database changes only through versioned migrations that run as a deploy step. Each one
  must be safe to run against production while the previous release is still serving
  (expand, migrate, contract).

## Releases

- Semantic versioning tags `vX.Y.Z`; notes from `gh release create --generate-notes`.
- A release is cut only from a `main` commit whose CI passed and whose development deploy
  succeeded.
