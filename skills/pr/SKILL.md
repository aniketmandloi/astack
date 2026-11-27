---
name: pr
description: Write or update a pull request description, then open or edit the PR - a summary, a file-by-file table, a Mermaid diagram of the changed flow, acceptance criteria with evidence, the review result, risk and blast radius, checks, and environment impact. build and fix call it once their review is clean. Use for "open a PR", "write the PR", "update the PR description".
argument-hint: "[pr]"
---

# PR

Turn a reviewed branch into a PR whose description a reviewer can trust at a glance. The
template is in `../../docs/github.md` under "Branches and pull requests". The **writer** agent
writes it (`../../docs/routing.md`).

1. **Gather the inputs**:
   - the issue it closes: its goal, acceptance criteria, and title
   - the base branch (the default branch) and the branch's head SHA
   - the builder's report, with its diagram sketch when there is one
   - the review result (`Reviewed at <sha>`), the checks run, and the deslop record
   - for a fix: the root cause

   **build** and **fix** pass all of these in. When it's called on its own, for a branch
   without those reports, send a **scout** for the diff summary, the tests the diff adds, and
   the checks' current results. Write the Review section as "not reviewed yet", and offer the
   **review** skill.
2. **Confirm the branch**:
   - The review covers this exact commit: the reviewed SHA is the branch's head. If it isn't,
     run the **review** skill first (a delta review) so the PR doesn't open on unreviewed code.
   - Push the branch (`git push -u origin <branch>`) if it isn't on the remote yet.
3. **Brief the writer** with every input, the template, the prose rules from
   `../../docs/slop.md`, the title (the issue's title), and whether to create the PR or edit an
   existing one.
4. **Check its work** before reporting:
   - the body opens with `Closes #<n>`
   - every acceptance criterion appears with evidence
   - the diagram, if there is one, names only components that exist in the diff
   - nothing in it contradicts the reports

   Send anything wrong back to the writer once. Fix it yourself if it's still wrong.
5. **Post the review** as the PR's first comment, with `gh pr review <pr> --comment` and the
   review result unchanged (`Reviewed at <sha>`, scope, verdict, and findings), so the merge
   gate in `../../docs/github.md` can find it.
6. Move the issue to `status:in-review`, and report the PR link.

When the PR already exists and its code changes later, rerun this skill to edit the body, so
the description keeps matching what will merge.
