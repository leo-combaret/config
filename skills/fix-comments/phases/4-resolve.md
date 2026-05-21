# Phase 4 - Resolve

Goal: act on `selected_items`: fix accepted feedback, reply to rejected or discussion items where appropriate, and resolve selected GitHub review threads.

Do not commit, push, merge, or revert unrelated changes.

## Resolution policy

- `ACCEPT`: make the code change, run focused validation, post a short reply if useful, then resolve the thread.
- `REJECT`: do not change code. Post a concise rationale reply, then resolve the thread if the user selected it or chose `proceed`.
- `DISCUSS`: post a clarification reply only if explicitly selected. Leave unresolved unless the user explicitly asked to resolve it.

If code changes are local and not pushed, still do not commit or push. Surface that the PR threads were resolved but code changes remain local.

## Step 1 - Group selected items by entrypoint

Group `selected_items` by `entrypoint`. Each worker should own one entrypoint, including all files needed for the selected comments in that entrypoint.

Spawn one `worker` per entrypoint before waiting. If using the local fallback, process one entrypoint at a time locally.

## Worker prompt template

````text
You are resolving selected PR review comments for one entrypoint.

Entrypoint: {{ENTRYPOINT_NAME}}

Selected items:
{{SELECTED_ITEMS_FOR_ENTRYPOINT}}

Selected items include comment indexes, thread IDs, primary database IDs when available, file paths, classifications, actual behavior examples, reflections, and recommendations.

You are not alone in the codebase. Do not revert unrelated edits or changes made by others. Work with current file contents.

Rules:
1. For ACCEPT items, read the relevant files, make the smallest defensible code changes, and preserve unrelated behavior.
2. For REJECT items, do not edit code unless the item also contains an accepted subpoint. Prepare a concise GitHub reply grounded in the actual behavior example, explaining the false premise or why no change is needed.
3. For DISCUSS items, prepare or post only the clarification requested by the user, grounded in the concrete scenario from the actual behavior example. Do not resolve unless explicitly told.
4. Do not add comments like `fixed comment #3` in code.
5. Do not commit or push.
6. List every file you changed.

GitHub actions:
1. Capture coordinates:
   ```bash
   PR_NUMBER=$(gh pr view --json number --jq '.number')
   REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
   OWNER=${REPO%/*}
   NAME=${REPO#*/}
   ```

2. To reply to a review comment when needed, use the selected item's primary database ID when available:
   ```bash
   gh api --method POST "repos/$REPO/pulls/$PR_NUMBER/comments/<databaseId>/replies" -f body="<reply body>"
   ```
   If only a GraphQL comment ID is available, resolve the thread and report that no REST reply was posted.

3. To resolve a review thread, use GraphQL:
   ```bash
   gh api graphql -f threadId="<thread id>" -f query='
   mutation($threadId: ID!) {
     resolveReviewThread(input: {threadId: $threadId}) {
       thread { id isResolved }
     }
   }'
   ```

4. Resolve only the thread IDs allowed by the resolution policy for each selected item.

Validation:
- Run the narrowest useful validation command for the files you changed: targeted tests, typecheck, lint, or a focused repo command.
- If validation is unavailable or too expensive, say why.

Return a short markdown report:
- For each selected comment index: fixed / replied / resolved / left unresolved / skipped, with one-sentence reason.
- Files changed.
- GitHub thread IDs resolved.
- Replies posted.
- Validation command and result.
````

## Step 2 - Integrate results

After all workers return:

1. Inspect changed files and worker reports.
2. Run any missing parent-level focused validation if useful.
3. Capture PR coordinates, then check unresolved status for selected threads when possible:
   ```bash
   PR_NUMBER=$(gh pr view --json number --jq '.number')
   REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
   OWNER=${REPO%/*}
   NAME=${REPO#*/}

   gh api graphql -f owner="$OWNER" -f name="$NAME" -F number="$PR_NUMBER" -f query='
   query($owner: String!, $name: String!, $number: Int!) {
     repository(owner: $owner, name: $name) {
       pullRequest(number: $number) {
         reviewThreads(first: 100) {
           nodes { id isResolved }
         }
       }
     }
   }'
   ```

## Step 3 - Final summary

Surface a concise summary:

```text
Handled N selected comment item(s).
Fixed: <indexes>
Rejected/replied: <indexes>
Discuss left open: <indexes>
Resolved threads: <count>
Validation: <command and result, or not run with reason>
```

List partial or skipped items and changed files. Remind the user that local fixes are not committed or pushed.
