---
name: fix-comments
description: Analyze and resolve unresolved GitHub PR review comments with PR-review discipline. Use when the user asks to fix PR comments, handle review feedback, address unresolved comments, or resolve GitHub review threads. If the user explicitly asks for subagents, parallel agents, or the deep workflow, coordinate Codex subagents for fetching comments, mapping architecture, classifying comment pertinence, fixing accepted feedback, and resolving review threads; otherwise perform the workflow locally or ask before spawning agents.
---

# Fix Comments

A Codex-compatible workflow for handling unresolved GitHub PR review comments.

This skill is not a blind "apply reviewer feedback" workflow. Review comments can be wrong, stale, unclear, or outside the PR scope. The review phase must classify each comment as `ACCEPT`, `REJECT`, or `DISCUSS` with evidence and a recommendation.

Codex subagents are opt-in. Spawn subagents only when the user's current request explicitly asks for agents, subagents, parallel review, or this deep workflow. If the user only asks to fix comments, use the same process locally, or ask whether they want the multi-agent version before spawning.

## Prerequisites

Before starting, confirm:
- The current branch has an open PR (`gh pr view` succeeds).
- The user is in the repo where the PR lives.
- GitHub CLI authentication can read PR review threads and resolve them.

If `gh pr view` fails, stop and ask the user which PR or base ref to use.

Respect the current working tree. Do not revert user changes, do not commit, and do not push unless the user explicitly asks.

## Codex subagent rules

When the multi-agent path is explicitly authorized:

- Use Codex `spawn_agent` and `wait_agent`, not legacy Agent specs.
- Prefer built-in agents: `default` for fetching, merging, aggregation, and GitHub API actions; `explorer` for read-heavy architecture mapping and comment pertinence review; `worker` for bounded fixes.
- Spawn independent agents before waiting when their tasks can run in parallel.
- Keep every subagent prompt self-contained: include exact commands, artifacts, and output shape.
- Do not duplicate work between parent and child agents. The parent orchestrates, integrates results, asks the user for decisions, and performs final verification.
- For code-editing workers, assign disjoint ownership by entrypoint. Tell workers they are not alone in the codebase, must not revert unrelated edits, and must list every changed file.
- Close completed agent threads when they are no longer needed if the tool is available.

When the multi-agent path is not authorized, follow the same four phases locally without spawning subagents.

## Workflow shape

```text
1. Fetch -> 2. Classify -> 3. Display -> 4. Resolve
```

Each phase is documented in its own file. Read the phase file when you reach that step; do not preload them all.

| Phase | File | Purpose |
| --- | --- | --- |
| 1. Fetch | `phases/1-fetch.md` | Fetch unresolved review threads, assign chronological indexes, map architecture, and merge comments into entrypoint packets. |
| 2. Classify | `phases/2-classify.md` | Review comment pertinence by entrypoint and classify each item as ACCEPT, REJECT, or DISCUSS. |
| 3. Display | `phases/3-display.md` | Present indexed results and ask whether to proceed, cherry-pick, or revise the analysis. |
| 4. Resolve | `phases/4-resolve.md` | Fix accepted feedback by entrypoint, reply where useful, and resolve selected GitHub review threads. |

## Start

Read `phases/1-fetch.md` and follow it.
