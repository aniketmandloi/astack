# Environments and delivery

The practices `setup` installs and `ship` relies on. Development and production are separate
environments with separate config, secrets, and data; code moves from one to the other only
through `main` and a release.

## Artifact kinds

What reaches a user decides what "deploy" means. `chart` settles it for every new project:
which artifact the user gets, and how to verify that exact artifact.

| Artifact | Development channel (every merge to `main`) | Production channel (a release tag) | Smoke check |
|---|---|---|---|
| Hosted web app or API | deploy to the development environment | deploy to production | health endpoint, then end-to-end smoke tests against the URL |
| Mobile app | an internal test build, on the store's test track | a store release | install the build on a simulator or device and run the main flow |
| CLI or library | a prerelease package or a build artifact | a publish to the registry, or binaries attached to the release | install the published artifact fresh and run its main command or import |
| Desktop or local-first app | a build artifact | a signed release | install it, launch it, and run the main flow |

The rest of this doc is written for hosted apps. For the other kinds, the same rules hold,
with "deploy" meaning "publish to the channel above". The health endpoint and deployed URL
become the smoke check in the table.

## Flow

```
issue branch ──PR + CI──▶ main ──push──▶ deploy: development (automatic)
                                 └─release vX.Y.Z──▶ deploy: production (gated)
```

- Trunk-based: `main` is always deployable; short-lived branch per issue; squash merge.
- Every merge to `main` deploys to **development**. A published GitHub release deploys that tag
  to **production**. The rollback is a manual run of the deploy workflow dispatched on an
  older release tag.
- PR previews, when the host offers them, deploy with development config and never touch
  production data.

## Config and secrets

- Twelve-factor: all config comes from environment variables. Nothing in code differs between
  environments.
- Commit `.env.example` with every variable name and a safe dummy value; gitignore `.env*`
  except that file.
- Deploy-time secrets are GitHub **environment secrets** (`gh secret set <NAME> --env
  development|production`), never repository secrets, so a development job cannot read a
  production secret. The one exception is the `prefixed` secrets mode, for plans without
  environments (see "Secrets mode" below).
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
  -F allow_rebase_merge=false -F delete_branch_on_merge=false
```
Merged branches are kept: deleting a branch is the user's call, so GitHub's automatic
deletion stays off. The setup report shows the repo's effective `delete_branch_on_merge`
(`gh api repos/{owner}/{repo} --jq .delete_branch_on_merge`), and on an existing repo it says
so if the setting was on before.

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

**Private repo on the free plan**: no environments or environment secrets exist. The user
chooses one of three options:
1. Make the repo public, which brings environments and rulesets on the free plan.
2. Upgrade to GitHub Pro.
3. Accept weaker isolation. Deploy jobs read repository secrets prefixed `DEV_` and `PROD_`,
   and the production job runs only on a release. Any workflow can read a production secret,
   so state that in the setup report and in `AGENTS.md`.

**Secrets mode**: `setup` records the outcome as the repo variable `ASTACK_SECRETS_MODE`
(`gh variable set ASTACK_SECRETS_MODE --body environments|prefixed`). Every step that touches
deploy secrets reads it, so hosting instructions, workflows, release checks, and rollback
agree:

| | `environments` | `prefixed` |
|---|---|---|
| Set a secret | `gh secret set <NAME> --env development` (or `production`) | `gh secret set DEV_<NAME>` / `gh secret set PROD_<NAME>` |
| List production secrets | `gh secret list --env production` | `gh secret list`, names starting `PROD_` |
| Deploy jobs | `environment: development` / `production` | no `environment:` key; each job maps `DEV_<NAME>` or `PROD_<NAME>` to `<NAME>` in its `env:` |
| Production gate | tag-only policy, plus a reviewer where the plan allows | the job's own `refs/tags/v` check, and only `ship` creates releases |

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
  install from the lockfile, format check, lint, typecheck, test, the end-to-end tests
  (`docs/app-checks.md`), build, and the slop gate from `docs/slop.md`. Commands come from the project's own scripts; the linter config, the
  unused-code detector, and the marker grep are added to the project if missing.
- `.github/workflows/deploy.yml`:
  - triggers: push to `main` → `development`; `release: published` → `production`;
    `workflow_dispatch` with no inputs → `production`, for rollback. A rollback is dispatched
    on the release tag itself (`gh workflow run deploy.yml --ref v1.2.3`). GitHub checks the
    run's own ref against production's tag-only policy, so a run dispatched from `main` with
    a tag passed as an input would be refused. The dispatched job fails unless `github.ref`
    starts with `refs/tags/v`, and it deploys exactly the revision it checked out.
  - each deploy job gets its secrets and gates the way the repo's `ASTACK_SECRETS_MODE` says
    (the "Secrets mode" table above): `environment:` in `environments` mode, and the
    `DEV_`/`PROD_` mapping with no `environment:` key in `prefixed` mode. Either way it sets
    `concurrency: deploy-<environment>` with `cancel-in-progress: false`.
  - the deploy step uses the host's official CLI or action. After deploying, it checks that the
    health endpoint reports the commit just deployed, then runs the end-to-end smoke tests
    against the deployed URL. It records that deployment's own URL, when the host gives each
    deployment one, in the job summary. The job fails
    if either fails.
- Every workflow: top-level `permissions: contents: read`, raised per job only where needed
  (`id-token: write` for OIDC, `deployments: write`). Third-party actions are pinned to a full
  commit SHA with the version in a trailing comment.
- `.github/dependabot.yml`: weekly updates for the project's package ecosystem and for
  `github-actions`.
- `.github/ISSUE_TEMPLATE/bug.yml` and `spec.yml` matching the bodies in `docs/github.md`, and
  `.github/pull_request_template.md` matching its PR body.
- `.env.example`, and `.gitignore` entries for `.env*`.
- The AStack block in `AGENTS.md` and the `@AGENTS.md` import in `CLAUDE.md`, as
  `docs/agents-md.md` describes, merged into any existing files.

## Application baseline (built by the walking-skeleton slice)

- A health endpoint (or the host's equivalent) that the deploy job checks. It reports the
  commit SHA it was built from, so anyone can confirm which build they're looking at.
- Structured logs, and error tracking tagged with the environment name.
- Database changes only through versioned migrations that run as a deploy step. Each one
  must be safe to run against production while the previous release is still serving
  (expand, migrate, contract).

## Releases

- Semantic versioning tags `vX.Y.Z`; notes from `gh release create --generate-notes`.
- A release is cut only from a `main` commit whose CI passed and whose development deploy
  succeeded.
- The first release has no previous tag, so its only recovery is fixing forward: **fix**, then
  a patch release. Releasing the walking skeleton early as `v0.1.0` means every release
  customers see has a rollback target.
- Rehearse once before the first customer, on a disposable app or right after the skeleton's
  second release: dispatch a rollback to the previous tag, confirm production serves it, then
  redeploy the current tag the same way.
