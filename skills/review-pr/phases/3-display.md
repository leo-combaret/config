# Phase 3 - Display

Goal: render the deduped issue list to the user and capture their decisions about scope and action.

You arrive here with the JSON from Phase 2.

## Step 1 - Render issues

Print this header first, derived from `totals`:

```text
Found X issues across Y files - N MUST · N SHOULD · N COULD
```

Then for each file in `files`:

```markdown
## `<path>` · <issue_count> issue(s)

**#<number>** · L<line> · **<priority>** · `<category>` · scope: `<scope>`
> <description>
**Fix:** <suggestion>
```

Rendering rules:
- Use the issue `number` verbatim. These are the IDs the user will reference.
- Use bold `**MUST**`, `**SHOULD**`, and `**COULD**`.
- If `suggestion` contains code, render it in a fenced code block.
- Keep this in the assistant message; do not write it to a file.
- If there are no issues, say that clearly, mention any residual test or review limitations, and stop the workflow.

## Step 2 - Ask what to act on

Codex question mechanics depend on the active runtime mode.

Use `request_user_input` only when that tool is available in the current mode. In Plan mode, it can ask one to three short questions and wait for a response. Each question must have 2-3 predefined options; the client adds a free-form Other option automatically, so do not add an `Other` option yourself.

When `request_user_input` is available, ask both decisions in one tool call:

```json
{
  "questions": [
    {
      "header": "Scope",
      "id": "issue_scope",
      "question": "Which issues do you want to address?",
      "options": [
        {
          "label": "MUST+SHOULD (Recommended)",
          "description": "Skip COULD-priority nits."
        },
        {
          "label": "All issues",
          "description": "Act on every issue listed."
        },
        {
          "label": "Specific issues",
          "description": "Use Other to enter numbers like 1, 3, 7-9."
        }
      ]
    },
    {
      "header": "Action",
      "id": "issue_action",
      "question": "How should I address the selected issues?",
      "options": [
        {
          "label": "Fix in code (Recommended)",
          "description": "Edit local files and leave the diff for review."
        },
        {
          "label": "Post comments",
          "description": "Submit inline GitHub review comments."
        }
      ]
    }
  ]
}
```

When `request_user_input` is not available, ask a concise plain-text question and stop:

```text
Which issues should I act on, and how?

Scope: `MUST + SHOULD` (recommended), `all`, or specific issue numbers like `1, 3, 7-9`.
Action: `fix` or `comment`.
```

Do not proceed to Phase 4 until the user has answered.

## Step 3 - Parse the answer

Resolve scope into a concrete list of issue objects:

- `MUST + SHOULD` -> every issue whose priority is `MUST` or `SHOULD`.
- `all` -> every issue.
- Specific issue numbers -> parse comma-separated numbers and ranges, for example `1, 3, 7-9`.

Validate every requested issue number exists. If any are invalid, list the invalid values and ask again.

Resolve action:

- `fix` / `Fix in code` -> `selected_action = "fix"`
- `comment` / `Post PR comments` -> `selected_action = "comment"`

Store the resolved issue objects as `selected_issues`.

## Step 4 - Hand off to Phase 4

Pass `selected_issues` and `selected_action` into Phase 4.

Read `phases/4-resolve.md`.
