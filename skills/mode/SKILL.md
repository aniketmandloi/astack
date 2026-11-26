---
name: mode
description: Autonomous AStack. Give it a goal (a new project idea, a feature in an existing app, a bug, a cleanup) and it drives that goal through every stage on its own - chart, decide, spec, slice, build, review, babysit, and merge to development - recording every decision on GitHub, pausing only for production, money, secrets, destructive actions, and calls only the user can make. Run it with no goal to resume an open run.
argument-hint: "[goal]"
disable-model-invocation: true
---

# AStack mode

Drive one goal through every AStack stage without waiting on the user, under the grant in
`../../docs/autonomy.md`. State lives on GitHub (`../../docs/github.md`), and every piece of
work goes to the routed agents (`../../docs/routing.md`), so the run survives context
compaction and new sessions. Run the main session on the strongest model, because it makes
the calls.

## Scope

A run works only on its **Scope**, which is recorded in the run issue:
- the map, spec, or issue that holds the goal
- their sub-issues
- every issue the run files itself, such as a bug from a failed deploy, added the moment it's
  filed

Unrelated open bugs, unlabelled issues, and other people's PRs are outside Scope, unless the
goal is about them ("triage the backlog", "fix the open bugs").

## 1. Start or resume

- **No goal**: find the open `astack:run` issue and resume from its Scope, Progress, and
  Waiting on you. If there's none, ask for a goal.
- **Goal given**: restate it in one sentence, with the smallest outcome that meets it. Create
  the run issue from the template in `../../docs/autonomy.md`, recording any narrowing the
  user gave. Tell the user the goal and the first step in two lines, then start without
  waiting.

Orient as the **astack** skill's step 1 does. If the repo isn't set up (`ASTACK_SETUP` isn't
`complete`), put `/astack:setup` in Waiting on you and stop.

## 2. Enter

Pick the entry by the goal's size, whether or not the repo already has an app. Record what it
creates as the run's Scope.

| Goal | Entry |
|---|---|
| A new project | **chart**, launch readiness included |
| A large or foggy change to an existing app | **chart**, no launch readiness unless the change is a new customer-facing product |
| Fits one session but has open decisions | **grill**, then **spec** |
| Clear and fits one session | **build**, which files the issue |
| A bug | **fix** |
| A behaviour-preserving cleanup | **build** in refactor mode |
| About the backlog itself | **triage**, and Scope is the issues it sorts |

## 3. Loop

Each turn, take the first item below that has work inside Scope, and run that skill with the
autonomy overrides.

1. **Open PRs first.** For any open PR that closes a Scope issue, including PRs opened by
   **fix**:
   - **review** it if its last verdict isn't at the current head
   - **babysit** it to merge-ready
   - merge it, pinned to the reviewed SHA
   - watch the deploy run for its merge commit (`../../docs/github.md`, "Commits, verdicts,
     and deploys")

   If that deploy fails, file an `astack:bug`, add it to Scope, and link it to the PR.
   Finish a PR in flight before claiming new work.
2. **Decision tickets**: work the map's frontier with **chart**. chart's one-ticket-per-session
   limit doesn't apply in a run, but reload the map from GitHub before each ticket. Research
   tickets go to scouts in parallel.
3. **A finished map with no spec**: **spec**.
4. **A spec whose Slice plan is missing or has unticked items**: **slice**.
5. **Scope bugs**: **fix**. Its PR goes through item 1 on the next turn.
6. **The next startable Scope slice**: **build** it. Its PR goes through item 1.

After each unit, update the run issue's Scope, Progress, Decided by astack mode, and Waiting
on you. Re-read the run issue rather than trusting memory once the conversation is long.

No gate is skipped in a run. Test-first, deslop, review, and CI all apply as they do in the
skills. When a unit fails the same way twice, stop working on it, record what was tried
under Waiting on you, and move on to the next unit.

## 4. Stop

What "met" means depends on the entry:

| Entry | Met when |
|---|---|
| chart, or grill then spec | every slice of the spec without `astack:release` is closed by a merged PR, and the deploy evidence for the last merge commit holds |
| build, fix, or refactor | its PR is merged, and the deploy evidence for its merge commit holds |

Deploy evidence is the deploy run for that commit succeeding. In a repo with no deploy
workflow AStack can track, it's the checks on that commit passing (`../../docs/footprint.md`).
| triage | every issue it was asked to sort has been classified and its changes applied, or held under Waiting on you |

Release-only work (`astack:release`, such as Connect production) never holds up a development
run. List it under Waiting on you for `ship`.

When the goal is met, **reconcile the parents**. Close the spec if all its sub-issues are
closed. Otherwise, comment on it that development is complete, listing the open release-only
items. The map is already closed once its spec was filed.

Stop when one of these is true:
- **The goal is met**, and the parents are reconciled.
- **Everything left in Scope waits on the user.**
- **The user's narrowing is reached.**

## 5. Report

The final reply, mirrored as a comment on the run issue:
- the goal
- what reached development, by PR title and link, with merge SHAs
- every decision the run made, by link, for the user to check or override
- Waiting on you, with exact commands or places, including deferred hands-on checks
- what was measured, and what remains unverified

When the goal is met and it had a spec, run the **retro** skill on that spec and include the
retro issue in the report. Close the run issue, and tell the user `/astack:ship` releases it.
