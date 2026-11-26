---
name: ship
description: Release main to production - check CI and the development deploy, review what changed and its environment impact, cut a semver GitHub release, and watch the gated production deploy, with rollback if it fails. Use when the user wants to release or deploy to production.
argument-hint: "[version]"
disable-model-invocation: true
---

# Ship

Production changes only through a release (`../../docs/environments.md`). Commands:
`../../docs/github.md`.

1. **Preflight.** Send a **scout** to gather, read-only:
   - the head of `main`, and whether its `ci` run passed and its development deploy succeeded
   - the last release tag, and the PRs merged since it, with their Environments sections
   - production secret names, listed the way the repo's `ASTACK_SECRETS_MODE` says
     (`../../docs/environments.md`), against the variables those PRs and `.env.example` need
   - open `astack:bug` issues in production, and whether the default-branch ruleset exists
     (create it now if CI exists and setup deferred it)
   - whether the **Connect production** slice is closed; stop if it isn't
   - open `astack:launch` issues
   - unticked "Checks for you" items on issues closed since the last release
     (`../../docs/app-checks.md`)
   Stop on a red CI run, a failed development deploy, or a missing production secret, and say
   what to do about each. Open launch issues don't block an early release like the walking
   skeleton's, but before the first release customers will use, list them and ship only on
   the user's explicit go-ahead.
2. **Plan the release.** Show the user: the changes by PR title, every migration and new
   variable, the rollback target (the previous tag; on the first release there is none, so
   say recovery means fixing forward), and a recommended version: major for
   breaking changes, minor for features, patch for fixes only. A version passed in wins.
3. **Release on their go-ahead**:
   `gh release create v<X.Y.Z> --target <main-sha> --generate-notes`. This starts the
   production deploy.
4. **Approve.** If production requires a reviewer, give the user the run link to approve in
   GitHub. Never approve it for them.
5. **Watch** the deploy run (`gh run watch <run-id>`) through its health check and the smoke
   tests against production.
6. **Failed?** Show the failing step's log and offer the rollback, dispatched on the previous
   tag so production's tag policy accepts it: `gh workflow run deploy.yml --ref
   <previous-tag>`. Watch that run too (`../../docs/environments.md`). On a first release,
   offer to fix forward instead. File an `astack:bug` issue for the failure.
7. **Report** the released version, its URL, the deploy run, and the health check result.
