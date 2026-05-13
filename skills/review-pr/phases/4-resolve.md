# Phase 4 - Resolve

Goal: act on `selected_issues` according to `selected_action` (`"fix"` or `"comment"`).

Do not commit, push, merge, or revert unrelated changes.

## Path A - Fix in code

Group `selected_issues` by file.

If subagents are authorized, spawn one `worker` per file before waiting. Each worker owns one file's fixes. If a fix requires edits outside its file, the worker must keep them minimal and explain why. Tell every worker it is not alone in the codebase, must not revert edits made by others, and must accommodate current file contents.

If subagents are not authorized, apply the fixes locally using the same ownership rule: finish one file at a time and keep edits scoped to selected issues.

### Worker prompt template

```text
You are fixing review issues in one file.

Ownership:
- Primary file: `{{FILE_PATH}}`
- Issues to fix:
{{ISSUES_FOR_FILE}}

You are not alone in the codebase. Do not revert unrelated edits or changes made by others. Work with current file contents.

Rules:
1. Read `{{FILE_PATH}}` first to ground edits in the current file.
2. Fix each selected issue with the smallest defensible change.
3. Do not edit other files unless required for type correctness or a directly coupled test update. If you do, explain why.
4. Do not add comments like `fixed issue #3`.
5. Do not commit.
6. Preserve unrelated formatting and behavior.

Return a short markdown report:
- For each issue number: applied / partial / skipped, with one-sentence reason.
- Every file path you changed.
- Any validation command you ran and its result.
```

After all workers return, inspect the changed files and run the narrowest useful validation available: targeted tests, typecheck, lint, or a focused command from the repo's docs/package scripts. If validation is too expensive or unavailable, say that.

Surface a concise summary:

```text
Fixed N of M selected issues across K files.
Validation: <command and result, or not run with reason>.
Review with `git diff` before committing.
```

List partial or skipped issues.

## Path B - Post inline PR comments

If subagents are authorized, spawn one `default` agent to batch every selected issue into a single GitHub review submission. If subagents are not authorized, do the same locally.

### Comment-poster prompt

````text
Post code review feedback as inline comments on the current PR. Use the GitHub Reviews API so all comments land in one review, not separate notifications.

## Selected issues
{{SELECTED_ISSUES_JSON}}

Each issue has: number, file path, line, priority, category, description, suggestion.

Steps:
1. Capture PR coordinates:
   ```bash
   PR_NUMBER=$(gh pr view --json number --jq '.number')
   COMMIT_ID=$(gh pr view --json headRefOid --jq '.headRefOid')
   REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
   ```

2. Build a JSON payload. For each selected issue, create one entry in `comments`:
   ```json
   {
     "commit_id": "<COMMIT_ID>",
     "event": "COMMENT",
     "body": "Automated review (N issues): X MUST · Y SHOULD · Z COULD",
     "comments": [
       {
         "path": "<file path>",
         "line": <line number as integer>,
         "side": "RIGHT",
         "body": "**[<PRIORITY>]** <Category> - <Description>\n\n**Suggested fix:**\n<suggestion>"
       }
     ]
   }
   ```

   If the issue spans a range like `42-58`, use the higher line number for `line` and include `"start_line": 42, "start_side": "RIGHT"`.

3. Write the payload to a temp file and post it:
   ```bash
   gh api --method POST "repos/$REPO/pulls/$PR_NUMBER/reviews" --input /tmp/pr-review.json
   ```

4. If the API call fails because a line cannot be anchored, drop only that comment and retry once. Report dropped comments.

Return a short report:
- Posted: issue numbers and inline comment URLs when available.
- Dropped: issue numbers that could not be anchored, with reasons.
- PR review URL when available.
````

After posting, surface the review URL and any dropped comments.

## Done

End the workflow. Do not commit, push, or merge.
