# Phase 1 - Fetch

Goal: produce a list of entrypoints - logically independent slices of the PR - each with enough context for a reviewer to evaluate it without re-reading the whole codebase.

Keep raw diffs and broad architecture notes out of the user-facing response. If the multi-agent path is authorized, put large reads in subagents and keep only summarized outputs in the parent session.

## Step 1 - Confirm PR coordinates

Run locally:

```bash
gh pr view --json number,title,body,author,baseRefName,headRefName,additions,deletions,changedFiles
```

If this fails, ask the user which PR or base ref to review. Do not continue on an assumed base.

## Step 2 - Collect PR facts and architecture

If subagents are authorized, spawn both fetchers before waiting.

### Agent A - PR fetcher

Use `spawn_agent` with `agent_type: "default"`.

Prompt:

```text
Gather full context on the current PR. Do not analyze or review; just collect facts.

Run these commands and return the relevant output:
1. `gh pr view --json number,title,body,author,baseRefName,headRefName,additions,deletions,changedFiles`
2. `gh pr diff`
3. `gh pr view --json files --jq '.files[] | {path, additions, deletions}'`

Return a single markdown report with these sections:
- Intent: PR title and description, trimmed of boilerplate.
- Stats: PR number, base/head branches, changed file count, +N/-M lines.
- Files changed: bulleted list with per-file +/- counts.
- Diff: full unified diff inside one fenced `diff` block.

No commentary, no review. Just the facts.
```

### Agent B - Architecture mapper

Use `spawn_agent` with `agent_type: "explorer"`.

Prompt:

```text
A PR is in flight on the current branch. Map the architectural shape of what changed so a reviewer can understand each slice without re-reading the repo.

Steps:
1. Run `gh pr view --json files --jq '.files[].path'` to get changed files.
2. For each changed file, identify:
   - Its role: route handler, React component, model, util, test, config, etc.
   - Direct importers or callers. Use `rg` for symbols and import paths.
   - Direct repo dependencies imported by the file.
   - Related tests: same directory, `.test.` / `.spec.` neighbors, fixtures, or integration tests.
3. Group changed files into ENTRYPOINTS: logically independent slices reviewable in isolation.
   A typical PR has 1-5 entrypoints. If the PR is one coupled change, return one entrypoint.

Read enough to understand call sites and tests, not the entire repo.

Return markdown with this exact shape:

## Entrypoints

### Entrypoint 1: <short name>
- Summary: 1-2 sentences on what this slice does and why it changed.
- Changed files:
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

If subagents are not authorized, run the same commands locally, use `rg` for callers/tests, and build the same two reports yourself.

## Step 3 - Merge into per-entrypoint packets

If subagents are authorized, spawn one `default` agent to fuse the PR facts and architecture map. Pass the full outputs from Agent A and Agent B into the prompt. If subagents are not authorized, do this merge locally.

Merger prompt:

````text
You are given:
1. A PR fetch report: intent, stats, changed files, full diff.
2. An architecture map grouping changed files into entrypoints with callers, dependencies, tests, and notes.

Produce one context packet per entrypoint. Each packet must be self-contained so a reviewer can read only that packet and review the slice.

Output exactly this shape, with no preamble:

## Packet 1: <entrypoint name>
**PR intent (relevant excerpt)**: <1-3 sentences from the PR description that pertain to this slice>
**Files in this slice**:
- `path` (+A/-D)
**Callers / dependencies / tests**:
<copied from the architecture map, trimmed to this slice>
**Diff for this slice**:
```diff
<only hunks from the full diff that touch files in this slice>
```
**Architectural notes**:
<copied from the architecture map>

## Packet 2: ...

Rules:
- Split the diff strictly by file membership in each entrypoint.
- Do not editorialize or review.
- If a file appears in multiple entrypoints, include the relevant hunks in each.

Here is input 1 - PR fetch report:
<paste Agent A output verbatim>

Here is input 2 - architecture map:
<paste Agent B output verbatim>
````

## Step 4 - Hand off to Phase 2

Keep the packet output in this session. It is the input to Phase 2. The raw diff and full architecture map can be discarded after the packets are available.

When packets are ready, read `phases/2-review.md`.
