---
name: triage
description: Sort new GitHub issues that have no astack label - customer reports, feature requests, questions, ideas - into AStack's shapes. Bugs become astack:bug issues with reproduction steps, clear requests become slices, larger ones go to grill or chart, and duplicates close with a link. Use for "triage", for issues without astack labels, or when feedback arrives after launch.
argument-hint: "[issue]"
---

# Triage

Conventions: `../../docs/github.md`. Routing: `../../docs/routing.md`.

1. **Collect**: the issue given, or every open issue without an `astack:` label:
   `gh issue list --state open --json number,title,labels,author --jq '[.[] | select([.labels[].name] | any(startswith("astack:")) | not)]'`.
2. **Investigate** with a **scout**: for each issue, find likely duplicates among open and
   closed issues, the code path involved, and recent PRs that touched it.
3. **Classify** each issue as one of:

   | Kind | Action |
   |---|---|
   | Bug | Rewrite the body into the bug shape, quoting the original. Label `astack:bug`. Note any missing detail |
   | Small, clear request | An `astack:slice` with acceptance criteria, `status:ready`, and a tier |
   | Request with open decisions | Comment that it needs decisions first, then route to **grill** and **spec** |
   | Large or foggy request | Route to **chart** |
   | Question | Draft an answer from the code and docs |
   | Duplicate | Comment with a link to the original, then close |
   | Out of scope | Draft the reason, citing the spec's or map's Out of scope |

4. **Show the table to the user**: each issue by title, its kind, and the action. Apply the
   changes they approve, using the **clerk** for three or more writes.
5. **Replies to people outside the repo** (a reporter's missing details, answers to
   questions, out-of-scope reasons) are drafts. Post them only on the user's go-ahead. In
   astack mode they go to Waiting on you (`../../docs/autonomy.md`). An out-of-scope close
   waits for the user, because it is a product call.
6. **Report** what was filed, labelled, routed, and closed, and what's waiting on the user.
