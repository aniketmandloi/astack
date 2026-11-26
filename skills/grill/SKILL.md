---
name: grill
description: Interview the user relentlessly about a plan, feature, design, or idea until every decision is settled. Use when the user says "grill me", wants to stress-test their thinking, or when a request has open decisions that must be settled before a spec. One session; for work too big for one session use chart instead.
---

# Grill

Interview the user until you reach a shared understanding. Map it as a **design tree**: every
decision branches into the decisions that hang off it.

## Rounds

The **frontier** is every decision whose prerequisites are already settled: the questions you
can ask now without guessing at answers you haven't heard. Ask the whole frontier in one round.
Number each question and give your recommended answer, worded so "yes" accepts it:

```
❓ **Q1** - **<question title>**: <question, with the options if there are several>

➡️ <your recommended answer>
```

Then wait. Each answer moves the frontier outward; recompute it and ask the next round. A
question whose answer depends on another question still open this round belongs to a later
round.

## Facts are yours, decisions are theirs

Never ask the user for a fact you can look up. When a frontier question needs one (what the
code does now, what an API supports, what a library costs), send it to the **scout** agent
(`../../docs/routing.md`). Don't wait on it: only the questions downstream of a running scout
wait, so ask the rest of the frontier now.

A "which approach" question whose answer you could observe by running something (behaviour,
speed, output, layout, whether a library handles the case) isn't the user's to answer either.
Settle it with a quick throwaway experiment: a **scout** for a check that only reads, the
**tweaker** on a `prototype/<slug>` branch for one that needs code. Bring the result to the
round. Only product and preference calls that no experiment can settle go to the user.

For a product or project, make sure the tree covers: who it is for and the outcome they get,
scope in and out, the riskiest assumption, data and integrations, how it is deployed and what
differs between development and production, and how you'll know it works.

## Done

The session is done when the frontier is empty: every branch visited, nothing silently
assumed. Play back the settled decisions as a short list and get the user's confirmation.

Then record the outcome on GitHub (`../../docs/github.md`): if the grilling was for an existing
issue, post the decisions as a comment on it. Otherwise hand the decisions to the skill that
called you, or offer to turn them into a spec with the **spec** skill.
