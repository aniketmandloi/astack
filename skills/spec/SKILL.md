---
name: spec
description: Write settled decisions up as a spec issue on GitHub, ready to slice into buildable work. Use after a grill session, when a chart map is done, or when the user describes a feature whose decisions are already clear. Input can be a map issue, an issue, or the decisions in the conversation.
argument-hint: "[map or issue]"
---

# Spec

A spec turns decisions into a contract that slices can be built against. It is a GitHub issue
labelled `astack:spec` with the body in `../../docs/github.md`.

1. **Gather the decisions.** From a map: its Decisions so far and the resolution comments they
   link (read with a **scout** agent when there are many). From an issue: its body and comments.
   From the conversation: what the user has confirmed.
2. **Fill the facts** the spec needs that nobody has stated (current code structure, the
   modules affected, API limits) with a **scout** agent rather than guessing.
3. **Find what's still open.** Every section must be answerable from the decisions. When one
   isn't, use the **grill** skill on just those questions. **Open questions** must be empty
   before the spec is filed.
4. **Write it.** Keep **Behaviour** to user-visible, testable statements; they become the
   slices' acceptance criteria. **Technical approach** names the modules, data model, and
   interfaces, not the code. **Environments** lists every new variable and secret per
   environment, any migration, and how to roll back (`../../docs/environments.md`).
5. **Show the draft to the user** and apply their corrections.
6. **File it**: create the issue; when it came from a map, make it a sub-issue of the map and
   post its link as the map's closing comment.

Then offer the **slice** skill.
