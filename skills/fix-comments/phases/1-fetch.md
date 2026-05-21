# Phase 1 - Fetch

Goal: produce entrypoint packets containing unresolved PR review comments, PR context, relevant diff hunks, and architecture notes.

Treat one unresolved GitHub review thread as one comment item. A thread may contain multiple messages; keep them together under one chronological index. Sort unresolved threads by the earliest comment `createdAt` ascending and assign indexes `1, 2, 3...`.

Keep raw API output and large diffs out of the user-facing response. Put large reads in subagents and keep only summarized packet output in the parent session. Use the local fallback only when subagent tools are unavailable or the user explicitly asked to run locally.

## Step 1 - Confirm PR coordinates

Run locally:

```bash
gh pr view --json number,title,body,author,baseRefName,headRefName,headRefOid,additions,deletions,changedFiles
```

If this fails, ask the user which PR or base ref to use.

## Step 2 - Fetch unresolved comments and architecture

Spawn both agents before waiting.

### Agent A - PR comment fetcher

Use `spawn_agent` with `agent_type: "default"`.

Prompt:

````text
Gather unresolved GitHub PR review comments and PR diff context. Do not classify or fix anything.

Steps:
1. Capture PR coordinates:
   ```bash
   PR_NUMBER=$(gh pr view --json number --jq '.number')
   REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
   OWNER=${REPO%/*}
   NAME=${REPO#*/}
   ```

2. Fetch PR metadata:
   ```bash
   gh pr view --json number,title,body,author,baseRefName,headRefName,headRefOid,additions,deletions,changedFiles
   gh pr view --json files --jq '.files[] | {path, additions, deletions}'
   gh pr diff
   ```

3. Fetch unresolved review threads with GraphQL. Use pagination if needed:
   ```bash
   gh api graphql -f owner="$OWNER" -f name="$NAME" -F number="$PR_NUMBER" -f query='
   query($owner: String!, $name: String!, $number: Int!) {
     repository(owner: $owner, name: $name) {
       pullRequest(number: $number) {
         reviewThreads(first: 100) {
           nodes {
             id
             isResolved
             path
             line
             startLine
             comments(first: 100) {
               nodes {
                 id
                 databaseId
                 author { login }
                 body
                 createdAt
                 url
                 path
                 line
                 originalLine
                 diffHunk
               }
             }
           }
         }
       }
     }
   }'
   ```

4. Keep only threads where `isResolved == false`.
5. Sort unresolved threads by the earliest `comments.nodes[].createdAt`.
6. Assign a stable local index starting at 1 in that chronological order.

Return one markdown report with these sections:

## PR
- Number:
- Title:
- Body excerpt:
- Base/head:
- Head SHA:
- Stats:

## Changed files
- `path` (+A/-D)

## Unresolved comments

### Comment #1
- Thread ID: <GraphQL reviewThread id>
- Primary comment ID: <first comment id>
- Primary database ID: <first databaseId if available>
- URL: <first comment url>
- File: `path`
- Line: <line or range>
- Created at: <timestamp of first comment>
- Author(s): <comma-separated logins>
- Diff hunk:
```diff
<diffHunk from primary comment if available>
```
- Comment text:
```text
<all messages in chronological order, each prefixed by author and timestamp>
```

### Comment #2
...

## Full PR diff
```diff
<full gh pr diff output>
```

Rules:
- Include only unresolved review threads.
- Preserve thread IDs and comment IDs exactly; Phase 4 needs them.
- Do not classify comments.
- Do not omit comments because they look wrong or stale.
````

### Agent B - Architecture mapper

Use `spawn_agent` with `agent_type: "explorer"`.

Prompt:

```text
A PR has unresolved review comments. Map the architectural shape of the commented files and changed files so comment reviewers can understand each slice.

Steps:
1. Run `gh pr view --json files --jq '.files[].path'` to get changed files.
2. Fetch unresolved review thread paths with `gh api graphql` or, if already available in the parent prompt, use that list.
3. For each commented or changed file, identify:
   - Its role: route handler, React component, model, util, test, config, etc.
   - Direct importers or callers. Use `rg` for symbols and import paths.
   - Direct repo dependencies imported by the file.
   - Related tests: same directory, `.test.` / `.spec.` neighbors, fixtures, or integration tests.
4. Group commented files and changed files into ENTRYPOINTS: logically independent slices reviewable and fixable together.
   A typical PR has 1-5 entrypoints. If the PR is one coupled change, return one entrypoint.

Read enough to understand call sites and tests, not the entire repo.

Return markdown with this exact shape:

## Entrypoints

### Entrypoint 1: <short name>
- Summary: 1-2 sentences on what this slice does.
- Changed/commented files:
  - `path/to/file.ts` - role
- Callers / consumers:
  - `path/to/caller.ts:LINE` - how it uses the changed code
- Dependencies pulled in:
  - `path/to/dep.ts` - what is imported
- Tests:
  - `path/to/file.test.ts` - what it covers, or "none found"
- Architectural notes: invariants, local patterns, gotchas a reviewer needs to know.

### Entrypoint 2: ...
```

Wait for both agents before merging.

If using the local fallback, run the same commands locally, use `rg` for callers/tests, and build the same two reports yourself.

## Step 3 - Merge into entrypoint packets

Spawn one `default` agent to merge the unresolved comments, PR diff, and architecture map. Pass the full outputs from Agent A and Agent B into the prompt. If using the local fallback, do this merge locally.

Merger prompt:

````text
You are given:
1. A PR comment fetch report containing PR context, changed files, unresolved indexed comments, thread IDs, comment IDs, and full diff.
2. An architecture map grouping changed/commented files into entrypoints.

Produce one context packet per entrypoint. Each packet must be self-contained so a comment reviewer can classify all comments in that slice.

Output exactly this shape, with no preamble:

## Packet 1: <entrypoint name>
**Files in this slice**:
- `path` (+A/-D)

**Comments in this slice**:

### Comment #<id>
- Thread ID: <thread id>
- Primary comment ID: <comment id>
- Primary database ID: <databaseId if available>
- URL: <url>
- File: `path`
- Line: <line or range>
- Author(s): <authors>
- Created at: <timestamp>
- Diff hunk:
```diff
<diff hunk>
```
- Comment text:
```text
<thread messages>
```

**Relevant PR diff for this slice**:
```diff
<only hunks from the full PR diff that touch files in this slice>
```

**Callers / dependencies / tests**:
<copied from architecture map, trimmed to this slice>

**Architectural notes**:
<copied from architecture map>

## Packet 2: ...

Rules:
- Preserve original comment indexes exactly.
- Put comments on the same entrypoint in the same packet.
- If multiple comments are materially the same concern in one entrypoint, keep all indexes in the packet; do not dedupe yet.
- Split PR diff strictly by file membership in each entrypoint.
- Do not classify or fix comments.

Here is input 1 - PR comment fetch report:
<paste Agent A output verbatim>

Here is input 2 - architecture map:
<paste Agent B output verbatim>
````

## Step 4 - Hand off to Phase 2

Keep the packet output in this session. It is the input to Phase 2. Raw API output and full diff can be discarded after packets are available.

If there are no unresolved comments, tell the user and stop the workflow.

When packets are ready, read `phases/2-classify.md`.
