# Slop

Slop is anything in a change that a careful senior engineer would delete in review. Nothing on
this list ships. Agents that write code get this file in their brief. Before a PR opens, a
deslop pass checks every diff except small contained ones against it. `review` checks every
PR against it and treats any hit as "changes needed".
CI enforces the mechanical rules (see "CI gate" below).

## Code

Each rule is checked against the diff, and a hit is reported with file:line. The one-line
versions in the `docs/agents-md.md` template must change whenever these do.

1. **Dead code.** Unused functions, exports, variables, imports, parameters, files, feature
   flags, or dependencies, including ones the change made unused.
2. **Commented-out code.** Delete it; git keeps history.
3. **Debug output.** `console.log`, `print`, `dbg!`, stray logging, `debugger`, and leftover
   test-only branches.
4. **Placeholders.** `TODO`, `FIXME`, `XXX`, `HACK`, stubs, `throw new Error("not implemented")`,
   fake data in non-test code. A deferred item becomes a GitHub issue, and the code links it.
5. **Speculative generality.** Options, config, interfaces, factories, or layers nobody asked
   for; a wrapper with one caller that adds nothing; "for future use".
6. **Reinvention.** A new helper, type, or dependency that duplicates one the codebase or its
   existing dependencies already have.
7. **Defensive noise.** Checks for states the types or callers already rule out; try/catch
   that swallows, logs and continues, or rethrows unchanged; fallbacks that hide a bug.
8. **Silenced tools.** `any`, unchecked casts, `@ts-ignore`, `eslint-disable`, `noqa`,
   `# type: ignore`, skipped tests, or loosened lint config used to make a check pass. Fix the
   cause. The only exception is a real external limitation, stated next to the suppression.
9. **Narrating comments.** Comments that restate the code, justify the change, or address the
   reviewer. A comment may say only what the code cannot show: an invariant, a gotcha, or a
   non-obvious reason.
10. **Hollow tests.** Tests that assert nothing meaningful, test the mock, pass without the
    change, or snapshot everything to avoid deciding what matters.
11. **Drive-by changes.** Reformatting, renames, or refactors outside the issue's scope.
12. **Style drift.** Naming, structure, error handling, or idioms that differ from the
    surrounding code.
13. **Vague names.** `data`, `info`, `handle`, `manager`, `util`, `helper`, `temp`, `result2`
    where a domain name exists.

## Prose

These rules apply to everything AStack writes: issues, PR bodies, comments, commit messages,
docs, and UI copy.

- State the fact, number, or instruction. Cut sentences that could appear unchanged in another
  project's docs.
- Plain words: "use" not "leverage" or "utilize"; "is" not "serves as"; no "delve", "crucial",
  "robust", "seamless", "comprehensive", "enhance", "pivotal", "landscape".
- No filler ("it's important to note", "in order to"), stacked hedges, generic conclusions,
  chatbot phrases ("Great question!", "I hope this helps"), or decorative emoji.
- No "not just X, but Y" framing, forced groups of three, or bold labels that restate their
  own line.
- Active voice with a named actor. Whole sentences, not arrow-and-abbreviation shorthand.
- Sentence-case headings. Straight quotes.

## CI gate

When AStack manages `ci` (`docs/footprint.md`), `setup` (or the walking-skeleton slice) wires
the mechanical rules into the required `ci` check, so a hit blocks the merge. When it doesn't,
the deslop pass and `review` enforce them instead. The gate is:

- The stack's linter, configured to fail on rules 1, 3, and 8: unused variables and imports,
  console or debug calls, explicit `any`, and suppression comments without a reason.
- The stack's unused-code and unused-dependency detector for rules 1 and 6 (for example knip
  for TypeScript, vulture and deptry for Python, `cargo udeps` for Rust). The scout confirms
  the current tool for the stack.
- A grep step over the PR's changed lines that fails on rule 4 markers without an issue
  link, and on merge-conflict markers.

The judgment rules (5, 6, 7, 9, 10, 11, 12, 13) can't be linted. The deslop pass and `review`
cover them.
