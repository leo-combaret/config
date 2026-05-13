# Phase 3 - Display

Goal: render the classified unresolved comments to the user and capture whether to proceed, cherry-pick, or revise the analysis.

You arrive here with the JSON from Phase 2.

## Step 1 - Render classifications

Print this header first, derived from `totals`:

```text
Analyzed X unresolved comment item(s): N ACCEPT, N REJECT, N DISCUSS
```

Then render every item in `items` order:

```markdown
#<comment ids> [<CLASSIFICATION>] <file>:<line>

**Comment:** <comment_summary>

**Reflection:** <reflection>

**Recommendation:** <recommendation>
```

Rendering rules:
- If an item groups multiple comments, render indexes as `#1, #4 [ACCEPT] path`.
- Keep classification labels uppercase.
- Show the file path in every header.
- If `recommendation` contains code, render it in a fenced code block.
- Keep this in the assistant message; do not write it to a file.
- If there are no unresolved comments, say that clearly and stop the workflow.

## Step 2 - Ask whether to proceed

Codex question mechanics depend on the active runtime mode.

Use `request_user_input` only when that tool is available in the current mode. In Plan mode, it can ask one to three short questions and wait for a response. Each question must have 2-3 predefined options; the client adds a free-form Other option automatically, so do not add an `Other` option yourself.

When `request_user_input` is available, ask one decision question:

```json
{
  "questions": [
    {
      "header": "Next Step",
      "id": "comment_action",
      "question": "How should I proceed with these comment classifications?",
      "options": [
        {
          "label": "Proceed (Recommended)",
          "description": "Fix ACCEPT items, reply to REJECT items, and leave DISCUSS for clarification."
        },
        {
          "label": "Cherry-pick",
          "description": "Use Other to enter specific comment indexes like 1, 3, 7-9."
        },
        {
          "label": "Revise analysis",
          "description": "Use Other to tell me what classification or reasoning to change."
        }
      ]
    }
  ]
}
```

When `request_user_input` is not available, ask a concise plain-text question and stop:

```text
Are you OK with this analysis and ready to proceed?

Reply with:
- `proceed` to fix ACCEPT items, reply to REJECT items, and leave DISCUSS for clarification.
- specific indexes like `1, 3, 7-9` to cherry-pick.
- your comments/corrections if you want the analysis revised first.
```

Do not proceed to Phase 4 until the user has answered.

## Step 3 - Parse the answer

Resolve the answer into `selected_items`:

- `proceed` -> select every `ACCEPT` and `REJECT` item. Do not select `DISCUSS` by default.
- Specific issue numbers -> select items whose `comment_ids` include those indexes.
- User corrections -> update classifications/recommendations if the requested changes are unambiguous; otherwise ask a follow-up question.

Default treatment by classification:

- `ACCEPT`: fix the code, reply that it was addressed, and resolve the review thread.
- `REJECT`: do not edit code; reply with the rejection rationale and resolve the review thread only if the user selected it or used `proceed`.
- `DISCUSS`: post or draft a clarification reply only when explicitly selected. Do not resolve unless the user explicitly asks.

Validate every requested comment index exists. If any are invalid, list the invalid values and ask again.

## Step 4 - Hand off to Phase 4

Pass `selected_items` into Phase 4.

Read `phases/4-resolve.md`.
