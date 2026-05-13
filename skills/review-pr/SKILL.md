---
name: review-pr-2
description: Code review the current PR or branch changes with PR-review discipline. Use whenever the user asks to review the PR, review changes, get PR feedback, or check the diff before merge. If the user explicitly asks for subagents, parallel agents, or the deep multi-agent workflow, coordinate Codex subagents for fetch, review, aggregation, and optional fixes; otherwise perform the review locally and ask before spawning agents.
---

# Review PR

A Codex-compatible PR review workflow with an optional multi-agent path.

Codex subagents are opt-in. Spawn subagents only when the user's current request explicitly asks for agents, subagents, parallel review, or this deep workflow. If the user only asks for a normal review, use the same review criteria locally, or ask whether they want the multi-agent version before spawning.

## Prerequisites

Before starting, confirm:
- The current branch has an open PR (`gh pr view` succeeds).
- The user is in the repo where the PR lives.

If `gh pr view` fails, stop and ask the user which PR or base ref to review.

Respect the current working tree. Do not revert user changes, do not commit, and do not push unless the user explicitly asks.

## Codex subagent rules

When the multi-agent path is explicitly authorized:

- Use Codex `spawn_agent` and `wait_agent`, not legacy Agent specs.
- Prefer built-in agents: `explorer` for read-heavy codebase mapping/review, `default` for fetching/aggregation/comment posting, and `worker` for bounded code fixes.
- Spawn independent agents before waiting when their tasks can run in parallel.
- Keep every subagent prompt self-contained: include the exact commands to run, artifacts to inspect, and output shape needed by the parent.
- Do not duplicate work between the parent and child agents. The parent orchestrates, integrates results, asks the user for decisions, and performs final verification.
- For code-editing workers, assign disjoint ownership by file or module. Tell workers they are not alone in the codebase, must not revert unrelated edits, and must list every changed file.
- Close completed agent threads when they are no longer needed if the tool is available.

When the multi-agent path is not authorized, follow the same four phases locally without spawning subagents.

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
