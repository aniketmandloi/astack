---
name: retro
description: Learn from finished work. When a spec's slices are all closed, or on demand for a date range, read its PRs, review findings, deslop rounds, CI fixes, failed checks, and the bugs that followed. Find the mistakes that happened more than once, and turn each into a guard - a structural change, a type, a lint rule, a test, or an AGENTS.md pitfall - filed as GitHub issues. Use for "retro", "what went wrong", after a spec closes, or when the same review finding keeps coming back.
argument-hint: "[spec | since <date>]"
---

# Retro

Conventions: `../../docs/github.md`. Routing: `../../docs/routing.md`.

1. **Scope**: the spec given, meaning the PRs that closed its slices. Otherwise the PRs merged
   since the last closed `astack:retro` issue, or since the date given.
2. **Gather** with a **scout**. For each PR, collect:
   - its review findings and verdicts
   - the Deslop section of its body
   - the CI failures and conflicts babysit fixed
   - failed "Checks for you" replies
   - `astack:bug` issues filed afterwards that trace back to it
3. **Find patterns**: group the findings by slop rule, failure kind, and module. A pattern is
   the same kind of mistake twice or more. List one-offs, but don't guard them.
4. **Pick a guard** for each pattern, the strongest that makes the mistake impossible, in this
   order:
   1. Change the structure so it can't happen.
   2. A type that rejects it.
   3. A lint rule whose message names the fix.
   4. A test.
   5. Last, a Pitfalls line in the AStack block of `AGENTS.md` (`../../docs/agents-md.md`).

   The guard's acceptance criterion is that it fails on a real instance of the old mistake,
   linked as evidence.
5. **Draft and show the user**:
   - a `Retro: <spec title>` issue labelled `astack:retro`, with Scope, Patterns (each with
     its evidence links and chosen guard), and One-offs
   - each guard as an `astack:slice` sub-issue with a tier and `status:ready`
   - all new Pitfalls lines together in one `tier:small` slice

   Create them on the user's approval, with the **clerk** for three or more.
6. **AStack's own share**: when a pattern traces back to an AStack skill step that misled the
   agent, say which step it was and suggest the change to AStack itself. Don't file that in
   this repo.
