# App checks

Two kinds of checking prove a change works in the running app.

- **CI tests** run on GitHub's machines and cost nothing locally, so they are always on. They
  are the end-to-end tests the builder writes for each user-facing slice, using the harness
  the walking skeleton sets up, plus the smoke test the deploy workflow runs after every
  deploy against the delivered artifact. For a hosted app that's the deployed URL; other
  artifact kinds are listed in `docs/environments.md`.
- **Hands-on checks** mean someone uses the app: clicks through the flow, tries the edge
  cases, and looks at the layout. An agent can only do this by driving a browser or the
  computer locally, which takes a lot of memory. So hands-on checks are off unless the user
  agrees.

## The preference

The preference is stored on GitHub as the repo variable `ASTACK_APP_CHECKS`, set to `agent`
or `manual`. Read it with `gh variable get ASTACK_APP_CHECKS`.

- **Unset**: the first time a hands-on check is needed, ask: "Should I run the app and check
  it myself? That needs browser automation and plenty of free memory. Or should I write the
  checks for you to run?" Save the answer with
  `gh variable set ASTACK_APP_CHECKS --body agent|manual`.
- **In astack mode, unset**: treat it as `manual`, and add the question to Waiting on you.
- The user can change it at any time with the same `gh variable set` command.

## `agent`

A hands-on check must run against the exact code it vouches for. The shared development URL
serves `main`, not the PR, so:

- **Before merge**: check only a PR preview whose deployment commit is the PR's head SHA.
- **No preview**: defer the checks until after the merge, once the deploy run for the merge
  commit has succeeded (`docs/github.md`, "Commits, verdicts, and deploys").
- **Start the app locally** only when nothing can be deployed. Say so first, and stop it
  afterwards.

Use the harness's browser automation. Post the results on the issue as the checklist below:
each check marked passed or failed, with what was seen and the commit SHA it ran against.

## `manual`

Post one comment on the issue, and link it from the PR:

```markdown
## Checks for you

Run it: <the PR preview URL for commit <head-sha>, or the development URL once the merge
commit <merge-sha> has deployed, or the exact local commands from AGENTS.md>

- [ ] **<check>**: <steps>. Expect: <result>. Covers: <acceptance criterion>
- [ ] ...

Reply with any check that fails, what you saw, and in which environment.
```

- Every user-visible acceptance criterion gets at least one check.
- For UI changes, add checks for the empty, loading, and error states, and for a narrow
  phone-width window.
- A reply reporting a failed check goes to the **fix** skill.

Unticked checks don't block a merge to development, which is where they get run. `ship` lists
any that are still unticked before a release.
