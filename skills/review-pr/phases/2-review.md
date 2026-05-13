# Phase 2 - Review

Goal: produce a deduplicated, ordered list of review issues grouped by file.

You arrive here with the packets from Phase 1. Each packet is self-contained. Give one packet to one reviewer, or review each packet locally if subagents were not authorized.

## Step 1 - Review each packet

If subagents are authorized, spawn one reviewer per packet before waiting. Use `agent_type: "explorer"` unless the reviewer needs to run project commands; then use `default`. Reviewers must not edit files.

Reviewer prompt template:

```text
You are reviewing one slice of a pull request. Be thorough, critical, and concrete. Find real risks, not generic style preferences.

## Context packet for this slice
{{PACKET}}

## Review criteria

Read the diff and use callers, dependencies, and tests in the packet to check whether the PR breaks contracts with the rest of the system.

For each changed hunk, evaluate:
- Correctness: logic errors, edge cases, error handling, type safety, data migrations, backward compatibility.
- Security: authz/authn mistakes, injection, unsafe deserialization, secret exposure, trust-boundary regressions.
- Performance: N+1 queries, accidental quadratic work, memory growth, blocking I/O, missing cache invalidation.
- Maintainability: broken local patterns, excessive duplication, unclear ownership, missing tests for changed behavior.

If a function signature, data shape, route contract, or side effect changed, verify likely callers and tests from the packet.

## Output format

For every issue you find, emit one block in exactly this shape:

Issue:
  File: <path from repo root>
  Line: <line number, or range like 42-58>
  Scope: <PR | IMPROVE>
  Category: <Correctness | Security | Performance | Maintainability>
  Priority: <MUST | SHOULD | COULD>
  Description: <what is wrong, in 1-3 sentences>
  Suggestion: <how to fix, with a code snippet if useful>

Rules:
- `PR` means introduced or materially changed by this PR.
- `IMPROVE` means pre-existing code touched by the diff.
- `MUST` is for bugs, security issues, data loss, or likely production regressions.
- `SHOULD` is for real maintainability, test, or edge-case risks worth fixing before merge.
- `COULD` is for low-risk cleanup. Do not emit style-only nits unless they hide a real issue.
- Cite real line numbers from the diff or surrounding file.
- One issue per block.
- If you find nothing, emit exactly: `No issues found in this slice.`
- Do not include praise, summaries, or unrelated commentary.
```

If subagents are not authorized, apply the same template yourself to each packet.

## Step 2 - Dedupe, group, and number

Once every reviewer has returned, aggregate findings. If subagents are authorized, this can be one `default` agent. Otherwise, do it locally.

Aggregator prompt:

````text
You are given N reviewer reports. Each contains zero or more Issue blocks in this shape:

Issue:
  File: <path>
  Line: <n>
  Scope: <PR|IMPROVE>
  Category: <...>
  Priority: <MUST|SHOULD|COULD>
  Description: <...>
  Suggestion: <...>

Do this in order:
1. Parse every Issue block.
2. Dedupe issues that target the same file, overlapping lines within roughly 3 lines, and the same root cause.
3. When merging duplicates, keep the highest priority and clearest description/suggestion. Mention if multiple reviewers flagged it.
4. Group by file path.
5. Order within each file by priority (MUST > SHOULD > COULD), then line ascending.
6. Order files by total issue count descending, then path ascending.
7. Number every issue sequentially across the final display order, starting at 1.

Return this exact JSON and nothing else:

```json
{
  "files": [
    {
      "path": "src/foo/bar.ts",
      "issue_count": 3,
      "issues": [
        {
          "number": 1,
          "line": "42",
          "scope": "PR",
          "category": "Security",
          "priority": "MUST",
          "description": "...",
          "suggestion": "..."
        }
      ]
    }
  ],
  "totals": { "must": 2, "should": 5, "could": 1 }
}
```

Reviewer reports follow.

===== Report 1 =====
<paste reviewer 1 output>

===== Report 2 =====
<paste reviewer 2 output>
````

## Step 3 - Hand off to Phase 3

Keep the aggregator JSON in this session. It is the input to Phase 3.

Read `phases/3-display.md`.
