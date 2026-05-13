# Phase 2 - Classify

Goal: critically review the pertinence of unresolved PR comments and classify each comment item as `ACCEPT`, `REJECT`, or `DISCUSS`.

You arrive here with entrypoint packets from Phase 1. Each packet contains all unresolved comments for one entrypoint. Give one packet to one reviewer, or classify locally if subagents were not authorized.

## Classification rules

Use these labels:

- `ACCEPT`: The comment identifies a real issue, useful improvement, missing test, or valid maintainability concern in the PR. The recommendation should explain what to change.
- `REJECT`: The comment is wrong, stale, already handled, based on a false premise, harmful, outside PR scope, or only a preference with no concrete value. The recommendation should explain how to respond and whether to resolve without code changes.
- `DISCUSS`: The comment may be valid but needs product, design, reviewer, or domain clarification before changing code. The recommendation should ask a specific question or propose a decision.

Be critical. Do not accept comments just because a reviewer wrote them. Use the PR diff, current file contents, callers, dependencies, tests, and local patterns as evidence.

## Step 1 - Classify each entrypoint packet

If subagents are authorized, spawn one `explorer` reviewer per packet before waiting. Reviewers must not edit files.

Reviewer prompt template:

```text
You are reviewing unresolved PR review comments for one entrypoint. Your job is to judge whether each comment is actually pertinent.

## Context packet
{{PACKET}}

## How to review

For each comment or group of materially duplicate comments:
1. Read the comment text and diff hunk.
2. Check the current file contents if needed.
3. Use callers, dependencies, tests, and local patterns from the packet to verify the premise.
4. Decide whether the comment should be ACCEPT, REJECT, or DISCUSS.
5. Give a concise reflection with evidence and a concrete recommendation.

Group comments only when they are the same concern in the same entrypoint. Preserve all original comment indexes in `CommentIds`.

## Output format

For every classified item, emit one block in exactly this shape:

CommentReview:
  CommentIds: [1]
  ThreadIds: ["<thread id>"]
  PrimaryDatabaseIds: [123456789]
  File: <path from repo root>
  Line: <line number or range>
  Classification: <ACCEPT | REJECT | DISCUSS>
  CommentSummary: <what the reviewer asked for, in 1-2 sentences>
  Reflection: <why this classification is correct, with concrete evidence>
  Recommendation: <what to do next; include code-level guidance for ACCEPT, reply guidance for REJECT/DISCUSS>

Rules:
- One block per comment or grouped duplicate concern.
- Preserve all comment indexes, thread IDs, and primary database IDs exactly.
- If a comment is wrong, say so clearly and explain the false premise.
- If a comment is unclear, classify as DISCUSS and state the exact clarification needed.
- Do not include praise or unrelated summaries.
```

If subagents are not authorized, apply the same template yourself to each packet.

## Step 2 - Aggregate and order results

Once every reviewer has returned, aggregate findings. If subagents are authorized, this can be one `default` agent. Otherwise, do it locally.

Aggregator prompt:

```text
You are given N comment pertinence reports. Each contains zero or more CommentReview blocks.

Do this in order:
1. Parse every CommentReview block.
2. Merge blocks that contain overlapping CommentIds or the same root concern on the same file and nearby lines.
3. When merging, preserve every CommentId, ThreadId, and PrimaryDatabaseId, keep the strongest evidence, and keep one final classification.
4. If merged reviewers disagree on classification, choose DISCUSS unless the evidence clearly supports ACCEPT or REJECT.
5. Order output by the lowest CommentId in each item.

Return this exact JSON and nothing else:

{
  "items": [
    {
      "comment_ids": [1],
      "thread_ids": ["PRRT_..."],
      "primary_database_ids": [123456789],
      "file": "src/foo/bar.ts",
      "line": "42",
      "classification": "ACCEPT",
      "comment_summary": "...",
      "reflection": "...",
      "recommendation": "...",
      "entrypoint": "Auth login flow"
    }
  ],
  "totals": { "accept": 2, "reject": 1, "discuss": 1 }
}

Reviewer reports follow.

===== Report 1 =====
<paste reviewer 1 output>

===== Report 2 =====
<paste reviewer 2 output>
```

## Step 3 - Hand off to Phase 3

Keep the aggregator JSON in this session. It is the input to Phase 3.

Read `phases/3-display.md`.
