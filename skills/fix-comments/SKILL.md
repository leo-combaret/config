---
name: fix-comments
description: Analyze and resolve unresolved GitHub PR review comments with PR-review discipline. Use when the user asks to fix PR comments, handle review feedback, address unresolved comments, or resolve GitHub review threads. This skill uses Codex subagents by default for fetching, architecture mapping, classification, and bounded fixes when subagent tools are available.
---

# Fix Comments

A Codex-compatible workflow for handling unresolved GitHub PR review comments.

This skill is not a blind "apply reviewer feedback" workflow. Review comments can be wrong, stale, unclear, or outside the PR scope. The review phase must classify each comment as `ACCEPT`, `REJECT`, or `DISCUSS` with evidence and a recommendation.

## Execution model

Use the subagent workflow described in the phase files by default. Invoking this skill means the user wants the comment workflow, including its fetcher, architecture mapper, classifier, merger, and worker agents where those agents are called for.

Fall back to the local, non-subagent path only when subagent tools are unavailable or when the user explicitly asks to run the workflow locally. Do not ask for a second authorization step before spawning the agents described by this skill.

## Prerequisites

Before starting, confirm:
- The current branch has an open PR (`gh pr view` succeeds).
- The user is in the repo where the PR lives.
- GitHub CLI authentication can read PR review threads and resolve them.

If `gh pr view` fails, stop and ask the user which PR or base ref to use.

Respect the current working tree. Do not revert user changes, do not commit, and do not push unless the user explicitly asks.

## Codex subagent rules

When using subagents:

- Use Codex `spawn_agent` and `wait_agent`, not legacy Agent specs.
- Prefer built-in agents: `default` for fetching, merging, aggregation, and GitHub API actions; `explorer` for read-heavy architecture mapping and comment pertinence review; `worker` for bounded fixes.
- Spawn independent agents before waiting when their tasks can run in parallel.
- Keep every subagent prompt self-contained: include exact commands, artifacts, and output shape.
- Do not duplicate work between parent and child agents. The parent orchestrates, integrates results, asks the user for decisions, and performs final verification.
- For code-editing workers, assign disjoint ownership by entrypoint. Tell workers they are not alone in the codebase, must not revert unrelated edits, and must list every changed file.
- Close completed agent threads when they are no longer needed if the tool is available.

When using the local fallback, follow the same four phases locally without spawning subagents.

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
