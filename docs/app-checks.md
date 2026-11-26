# App checks

Two kinds of checking prove a change works in the running app.

- **CI tests** run on GitHub's machines and cost nothing locally, so they are always on. They
  are the end-to-end tests the builder writes for each user-facing slice, using the harness
  the walking skeleton sets up, plus the smoke test the deploy workflow runs against the
  deployed URL after every deploy.
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

Check against the deployed development URL, or a PR preview when the host provides one,
using the harness's browser automation. Start the app locally only when nothing is
deployed. Say so first, and stop it afterwards. Post the results on the issue as the
checklist below, each check marked passed or failed, with what was seen.

## `manual`

Post one comment on the issue, and link it from the PR:

```markdown
## Checks for you

Run it: <the exact commands from AGENTS.md, or the development URL once deployed>

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
