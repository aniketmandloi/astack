---
name: mode
description: Autonomous AStack. Give it a goal (a new project idea, a feature, a cleanup) and it drives the whole pipeline on its own - chart, decide, spec, slice, build, review, and merge to development - recording every decision on GitHub, pausing only for production, money, secrets, destructive actions, and calls only the user can make. Run it with no goal to resume an open run.
argument-hint: "[goal]"
disable-model-invocation: true
---

# AStack mode

Drive a goal through every AStack stage without waiting on the user, under the grant in
`../../docs/autonomy.md`. State lives on GitHub (`../../docs/github.md`) and every piece of
work goes to the routed agents (`../../docs/routing.md`), so the run survives context
compaction and new sessions. Run the main session on the strongest model; it makes the calls.

## 1. Start or resume

- **No goal**: find the open `astack:run` issue and resume from its Progress and Waiting on
  you. If there is none, ask for a goal.
- **Goal given**: restate it in one sentence with the smallest outcome that meets it. Create
  the run issue from the template in `../../docs/autonomy.md`, recording any narrowing the
  user gave. Tell the user the goal and the first step in two lines, then start without
  waiting.

Orient as the **astack** skill's step 1 does. If the repo isn't set up, put `/astack:setup`
in Waiting on you and stop: nothing runs without the labels.

## 2. Loop

Each turn of the loop, take the earliest stage that has work, then run that skill with the
autonomy overrides:

1. A repo with no application code and no map: **chart** the goal (the launch readiness
   items included). For a goal that fits one session, use **grill** then **spec** instead.
2. Frontier decision tickets on the run's map: resolve them with **chart**. chart's
   one-ticket-per-session limit doesn't apply in a run, but reload the map from GitHub before
   each ticket. Research tickets go to scouts in parallel.
3. A finished map with no spec: **spec**.
4. A spec with no slices: **slice**.
5. Open issues with no `astack:` label: **triage**. Then any open `astack:bug`: **fix**.
6. Startable slices: **build** the next one, **review** it, **babysit** it to merge-ready,
   and merge it once it passes the gates in `../../docs/autonomy.md`. Then confirm its development deploy succeeded
   (`gh run list --workflow deploy.yml --branch main --limit 1`). If the deploy failed, file
   the failure as an `astack:bug`.

After each unit, update the run issue: Progress, Decided by astack mode, and Waiting on you.
Re-read the run issue rather than trusting memory when the conversation has grown long.

No gate is skipped in a run: test-first, deslop, review, and CI all apply as in the skills.
When a unit fails the same way twice, stop working on it, record what was tried under
Waiting on you, and move to the next unit.

## 3. Stop

Stop when one of these is true:
- **The goal is met**: every slice of its spec is closed, and the development deploy is green.
- **Everything left waits on the user.**
- **The user's narrowing is reached.**

## 4. Report

The final reply, mirrored as a comment on the run issue:
- the goal
- what reached development, by PR title and link
- every decision the run made, by link, for the user to check or override
- Waiting on you, with exact commands or places
- what was measured, and what remains unverified

When the goal is met, run the **retro** skill on its spec and include the retro issue in the
report. Close the run issue, and tell the user `/astack:ship` releases it.
