"""AStack guard: a Claude Code PreToolUse hook that denies destructive Bash commands.

Reads the hook payload on stdin and prints a deny decision for commands that force-push,
delete branches, recursively delete outside the working directory, delete GitHub
resources, or drop database objects. The user can still run any of them with `! <command>`.
"""

import json
import os
import re
import shlex
import sys

SEGMENT_SPLIT = re.compile(r"&&|\|\||[;|\n]")
SQL_DESTRUCTIVE = re.compile(r"\b(drop\s+(table|database|schema)|truncate\s+(table\s+)?\w)", re.I)
SQL_CLIENTS = {"psql", "mysql", "mariadb", "sqlite3", "sqlcmd", "duckdb", "cockroach", "clickhouse-client"}
PROTECTED_BRANCH = re.compile(r"(^|:)(refs/heads/)?(main|master)$")


def tokens(segment):
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def after(words, command):
    """Words following the first occurrence of `command` as a whole word, or None."""
    for i, word in enumerate(words):
        if os.path.basename(word) == command:
            return words[i + 1:]
    return None


def check_git(args):
    if not args:
        return None
    sub, rest = args[0], args[1:]
    if sub == "push":
        lease = any(a.startswith("--force-with-lease") or a == "--force-if-includes" for a in rest)
        bare_force = any(a in ("--force", "-f") or (re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*", a) and not a.startswith("--")) for a in rest)
        if bare_force or any(a.startswith("+") for a in rest):
            return "force-push without --force-with-lease"
        if lease and any(PROTECTED_BRANCH.search(a) for a in rest):
            return "force-push to main"
        if "--delete" in rest or "-d" in rest or any(a.startswith(":") and len(a) > 1 for a in rest):
            return "deleting a remote branch"
    if sub == "branch" and any(a in ("-d", "-D", "--delete") for a in rest):
        return "deleting a branch"
    return None


def check_rm(args, cwd):
    flags = [a for a in args if a.startswith("-")]
    targets = [a for a in args if not a.startswith("-")]
    letters = "".join(f.lstrip("-") for f in flags if not f.startswith("--"))
    recursive = "r" in letters.lower() or "--recursive" in flags
    force = "f" in letters or "--force" in flags
    if not (recursive and force):
        return None
    root = os.path.realpath(cwd)
    for target in targets:
        expanded = os.path.expandvars(os.path.expanduser(target))
        path = os.path.realpath(os.path.join(root, expanded))
        if path == root or os.path.commonpath([root, path]) != root:
            return "rm -rf outside the working directory: " + target
    return None


def check_gh(args):
    if args[:2] in (["repo", "delete"], ["release", "delete"], ["issue", "delete"]):
        return "gh " + " ".join(args[:2])
    if args[:1] == ["api"]:
        joined = " ".join(args)
        if re.search(r"(-X|--method)\s*=?\s*DELETE\b", joined, re.I):
            return "gh api DELETE request"
    return None


def reason_to_block(command, cwd):
    segments = [tokens(s.strip()) for s in SEGMENT_SPLIT.split(command)]
    # SQL only counts when a database client runs it; prose in an issue body or commit
    # message that mentions DROP TABLE is not a database operation.
    runs_sql_client = any(os.path.basename(w) in SQL_CLIENTS for words in segments for w in words)
    if runs_sql_client and SQL_DESTRUCTIVE.search(command):
        return "dropping or truncating database objects"
    for words in segments:
        for name, check in (("git", check_git), ("gh", check_gh)):
            args = after(words, name)
            if args is not None:
                reason = check(args)
                if reason:
                    return reason
        args = after(words, "rm")
        if args is not None:
            reason = check_rm(args, cwd)
            if reason:
                return reason
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return
    if payload.get("tool_name") != "Bash":
        return
    command = payload.get("tool_input", {}).get("command", "")
    reason = reason_to_block(command, payload.get("cwd") or os.getcwd())
    if reason:
        message = (
            "Blocked by the AStack guard: " + reason + ". If this is really intended, ask the "
            "user to run it themselves with `! " + command + "`."
        )
        json.dump({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": message,
            },
            "systemMessage": message,
        }, sys.stdout)


if __name__ == "__main__":
    main()
