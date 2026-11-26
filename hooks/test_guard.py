import json
import os
import subprocess
import sys
import tempfile
import unittest

GUARD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard.py")


def decision(command, cwd):
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}, "cwd": cwd})
    out = subprocess.run([sys.executable, GUARD], input=payload, capture_output=True, text=True, check=True).stdout
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "allow"


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()

    def assertDenied(self, command):
        self.assertEqual(decision(command, self.repo), "deny", command)

    def assertAllowed(self, command):
        self.assertEqual(decision(command, self.repo), "allow", command)

    def test_force_push(self):
        self.assertDenied("git push --force origin 12-login")
        self.assertDenied("git push -f")
        self.assertDenied("git push origin +12-login")
        self.assertDenied("git push --force-with-lease origin main")
        self.assertAllowed("git push --force-with-lease origin 12-login")
        self.assertAllowed("git push -u origin 12-login")

    def test_branch_deletion(self):
        self.assertDenied("git push origin --delete 12-login")
        self.assertDenied("git push origin :12-login")
        self.assertDenied("git branch -D 12-login")
        self.assertDenied("git branch -d 12-login")
        self.assertDenied("git branch --delete 12-login")
        self.assertAllowed("git branch 12-login")
        self.assertAllowed("git branch --show-current")

    def test_ordinary_git(self):
        self.assertAllowed("git status && git diff origin/main...HEAD")
        self.assertAllowed("git fetch origin && git rebase origin/main")
        self.assertAllowed('git commit -m "Remove the -f flag from the docs"')
        self.assertAllowed("git checkout -b 12-login origin/main")
        self.assertAllowed("git log --oneline -5 | cat")

    def test_rm(self):
        self.assertDenied("rm -rf /")
        self.assertDenied("rm -rf ~")
        self.assertDenied("rm -rf ..")
        self.assertDenied("rm -rf .")
        self.assertDenied("rm -fr /tmp/elsewhere")
        self.assertDenied("cd app && rm -r -f ../other")
        self.assertAllowed("rm -rf node_modules dist")
        self.assertAllowed("rm -r build")
        self.assertAllowed("rm notes.txt")

    def test_github_deletes(self):
        self.assertDenied("gh repo delete owner/repo --yes")
        self.assertDenied("gh release delete v1.0.0")
        self.assertDenied("gh api -X DELETE repos/o/r/issues/1/labels/x")
        self.assertDenied("gh api --method=DELETE repos/o/r/rulesets/1")
        self.assertAllowed("gh api -X POST repos/o/r/issues/1/sub_issues -F sub_issue_id=2")
        self.assertAllowed("gh issue close 4")

    def test_sql(self):
        self.assertDenied('psql "$DATABASE_URL" -c "DROP TABLE users"')
        self.assertDenied("echo 'truncate table orders;' | psql")
        self.assertDenied("sqlite3 app.db 'drop table sessions'")
        self.assertAllowed("psql -c 'select * from users'")
        self.assertAllowed('gh issue create --title "Migration" --body "This migration must not DROP TABLE users"')
        self.assertAllowed('git commit -m "Document why we never truncate table orders"')
        self.assertAllowed("grep -rn 'DROP TABLE' migrations/")

    def test_other_tools_and_bad_input(self):
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "/"}})
        out = subprocess.run([sys.executable, GUARD], input=payload, capture_output=True, text=True, check=True).stdout
        self.assertEqual(out, "")
        out = subprocess.run([sys.executable, GUARD], input="not json", capture_output=True, text=True, check=True).stdout
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
