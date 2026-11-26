---
name: fix
description: Fix a bug through GitHub - make sure an astack:bug issue with reproduction steps exists, reproduce it with a failing test, fix the root cause through the right-tier agent, and open a PR that closes the issue. Use when the user reports a bug, an error, a regression, or a failing behaviour in development or production.
argument-hint: "[bug issue | description]"
---

# Fix

Conventions: `../../docs/github.md`. Routing: `../../docs/routing.md`.

1. **Get the bug issue.** Use the one given, or file an `astack:bug` issue from the user's
   report with the bug body. Ask only for what you can't find yourself: send a **scout** for
   logs, recent commits and PRs, CI runs, and the code path.
2. **Production first?** If it's in production and hurting users, offer a rollback to the
   previous release (`../../docs/environments.md`) before the fix. The user decides.
3. **Claim and branch** as in the **build** skill.
4. **Reproduce, then fix.** Brief the **builder** agent (the **tweaker** only when the cause is
   already known and contained) to write a failing test that reproduces the bug first, then
   find the root cause and fix it there, not at the symptom. If it can't reproduce, have it
   report what it tried. Post that on the issue and ask the user for the missing detail rather
   than guessing at a fix.
5. **Verify and deslop** as in the **build** skill: the reproducing test now passes, the rest
   of the suite still passes, the diff touches only what the root cause needs, and a deslop
   pass comes back clean.
6. **Open the PR** closing the issue, with a short root-cause section: what was wrong, why, and
   why the fix is in the right place. Move the issue to `status:in-review`.
7. **Hands-on checks** for a user-facing bug, as in the **build** skill
   (`../../docs/app-checks.md`): the reproduction steps become the first check, and the
   expected result is the fixed behaviour.
