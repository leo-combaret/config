---
name: review-pr
description: Code review the current PR or branch changes with PR-review discipline. Use whenever the user asks to review the PR, review changes, get PR feedback, or check the diff before merge. This skill uses Codex subagents by default for PR context fetching, architecture mapping, per-entrypoint review, aggregation, and bounded fixes when subagent tools are available.
---

# Review PR

A Codex-compatible PR review workflow with a subagent-first execution path.

## Execution model

Use the subagent workflow described in the phase files by default. Invoking this skill means the user wants the review workflow, including its PR fetcher, architecture mapper, per-entrypoint reviewers, aggregator, and worker or comment-poster agents where those agents are called for.

Fall back to the local, non-subagent path only when subagent tools are unavailable or when the user explicitly asks to run the workflow locally. Do not ask for a second authorization step before spawning the agents described by this skill.

## Prerequisites

Before starting, confirm:
- The current branch has an open PR (`gh pr view` succeeds).
- The user is in the repo where the PR lives.

If `gh pr view` fails, stop and ask the user which PR or base ref to review.

Respect the current working tree. Do not revert user changes, do not commit, and do not push unless the user explicitly asks.

## Codex subagent rules

When using subagents:

- Use Codex `spawn_agent` and `wait_agent`, not legacy Agent specs.
- Prefer built-in agents: `explorer` for read-heavy codebase mapping/review, `default` for fetching/aggregation/comment posting, and `worker` for bounded code fixes.
- Spawn independent agents before waiting when their tasks can run in parallel.
- Keep every subagent prompt self-contained: include the exact commands to run, artifacts to inspect, and output shape needed by the parent.
- Do not duplicate work between the parent and child agents. The parent orchestrates, integrates results, asks the user for decisions, and performs final verification.
- For code-editing workers, assign disjoint ownership by file or module. Tell workers they are not alone in the codebase, must not revert unrelated edits, and must list every changed file.
- Close completed agent threads when they are no longer needed if the tool is available.

When using the local fallback, follow the same four phases locally without spawning subagents.

## Workflow shape

```
1. Fetch ──▶ 2. Review ──▶ 3. Display ──▶ 4. Resolve
```

Each phase is documented in its own file. Read the phase file when you reach that step; do not preload them all.

| Phase | File | Purpose |
| --- | --- | --- |
| 1. Fetch | `phases/1-fetch.md` | Pull PR diff/intent and map architecture in parallel; merge into per-entrypoint context packets. |
| 2. Review | `phases/2-review.md` | Spawn one reviewer per entrypoint in parallel; dedupe and group findings. |
| 3. Display | `phases/3-display.md` | Present grouped issues; ask the user which to act on and how. |
| 4. Resolve | `phases/4-resolve.md` | Either patch the code or post inline GitHub comments, based on the user's choice. |

## Start

Read `phases/1-fetch.md` and follow it.
