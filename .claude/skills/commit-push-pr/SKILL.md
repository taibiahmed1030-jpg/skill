---
name: commit-push-pr
description: "End-of-task git workflow. Writes the commit message, pushes the branch, opens the PR with a structured description."
---

Commit all staged and unstaged changes, push to remote, and open a pull request.

Steps:
1. Run `git status` and `git diff` to understand what changed
2. Run `git log --oneline -5` to understand recent commit style in this repo
3. Stage all relevant changes: `git add` specific files (avoid .env, secrets, node_modules)
4. Write a concise commit message focused on WHY, not what. Format:
   ```
   git commit -m "$(cat <<'EOF'
   <summary of change>

   EOF
   )"
   ```
5. Push: `git push` (or `git push -u origin HEAD` if no upstream)
6. Create PR with `gh pr create` using this format:
   ```
   gh pr create --title "<short title under 70 chars>" --body "$(cat <<'EOF'
   ## Summary
   - <bullet 1>
   - <bullet 2>

   ## Test plan
   - [ ] <manual test step>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```
7. Return the PR URL

Do not push to main/master without confirmation. If pre-commit hooks fail, fix the issue before retrying — never use --no-verify.
