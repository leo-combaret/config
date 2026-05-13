# Project Panel
The project panel shows a tree view of your workspace's files and directories. Toggle it with project panel: toggle focus ( cmd-shift-e|ctrl-shift-e ), or click the Project Panel button in the status bar.
## Navigating
Use the arrow keys to move through entries. right|right expands a directory and left|left collapses it. cmd-left|ctrl-left collapses every directory at once. Press space|space or click to preview a selected file, without giving it a permanent tab. Editing the file or double-clicking it promotes it to a permanent tab.
### Auto-reveal
By default, switching files in the editor will automatically highlight it in the project panel and scroll it into view. This can be disabled with the project_panel.auto_reveal_entries setting.
### Sticky Scroll
When project_panel.sticky_scroll is enabled (the default), ancestor directories pin themselves to the top of the panel as you scroll, so you always know which directory you're on.
### Directory Folding
When project_panel.auto_fold_dirs is enabled (the default), chains of directories that each contain a single child directory are collapsed into one row (for example, src/utils/helpers instead of three separate levels). Right-click a folded directory and choose Unfold Directory to expand the chain, or Fold Directory to collapse it again.
## Selecting Multiple Entries
Hold shift while pressing the up/down arrow keys to mark additional entries. Most file operations, like cut, copy, trash, delete and drag, apply to the full set of marked entries.
When exactly two files are marked, project panel: compare marked files ( alt-d|alt-d ) opens a diff view comparing them.
## File Operations
Right-click an entry to see the full list of available operations, or use the keybindings below.
### Creating Files and Directories
- project panel: new file ( cmd-n|ctrl-n ) creates a new file inside the selected directory.
- project panel: new directory ( alt-cmd-n|alt-ctrl-n ) creates a new directory.
An inline editor appears so you can type the name. Press enter to confirm or escape to cancel.
### Renaming
Press f2|f2 to rename the selected entry. The filename stem is pre-selected so you can type a new name without accidentally changing the extension. Press enter to confirm or escape to cancel.
### Cut, Copy, and Paste
- project panel: cut ( cmd-x|ctrl-x ) marks entries for moving.
- project panel: copy ( cmd-c|ctrl-c ) marks entries for copying.
- project panel: paste ( cmd-v|ctrl-v ) places them in the selected directory.
When pasting would create a name conflict, Zed appends a "copy" suffix (e.g., file copy.txt , file copy 2.txt ). If a single file is pasted with a generated suffix, the rename editor opens automatically so you can adjust the name.
### Duplicate
project panel: duplicate ( cmd-d| ) copies and pastes the selected entries in one step.
### Trash and Delete
- project panel: trash ( cmd-backspace|delete ) moves entries to the system trash.
- project panel: delete ( cmd-alt-backspace|ctrl-delete ) permanently deletes entries.
Both actions show a confirmation prompt listing the affected files. If any of the files have unsaved changes, the prompt warns you.
### Drag and Drop
Drag entries within the panel to move them. Hold alt while dropping to copy instead of move. You can also drag files from your operating system's file manager into the project panel to copy them into the project. Drag and drop can be disabled with the project_panel.drag_and_drop setting.
## Git Integration
When project_panel.git_status is enabled (the default), file and directory names are tinted to reflect their git status—modified, added, deleted, untracked, or conflicting.
Setting project_panel.git_status_indicator to true (disabled by default) adds a letter badge next to each name: M (modified), A (added), D (deleted), U (untracked) or ! (conflict).
Use project panel: select next git entry and {#action project_panel::SelectPrevGitEntry} to jump between tracked files with uncommitted changes. The right-click menu also offers Restore File to discard changes and View File History to browse a file's commit log.
## Diagnostics
The project_panel.show_diagnostics setting controls whether error and warning indicators appear on file and folder icons. Set it to "all" to see both errors and warnings, "errors" for errors only, or "off" to hide them. Diagnostics propagate upward—if a file deep in a directory has an error, its ancestor folders show an indicator too.
Enable project_panel.diagnostic_badges (disabled by default) to display numeric error and warning counts next to each entry. Use project panel: select next diagnostic and project panel: select prev diagnostic to navigate between files that have diagnostics.
See also Diagnostics & Quick Fixes for editor and tab diagnostic settings.
## Filtering and Sorting
### Hiding Files
- project_panel.hide_gitignore hides files matched by .gitignore . Toggle this with project panel: toggle hide git ignore .
- project_panel.hide_hidden hides dotfiles and other hidden entries. Toggle with project panel: toggle hide hidden .
### Sorting
The project_panel.sort_mode setting controls grouping:
- "directories_first" (default) — directories appear before files at each level.
- "files_first" — files appear before directories.
- "mixed" — directories and files are sorted together.
The project_panel.sort_order setting controls name comparison:
- "default" — case-insensitive natural sort ( file2 before file10 ).
- "upper" — uppercase names grouped first, then lowercase.
- "lower" — lowercase names grouped first, then uppercase.
- "unicode" — raw Unicode codepoint order with no case folding.
## Other Actions
- project panel: reveal in file manager ( alt-cmd-r|alt-ctrl-r ) reveals the selected entry in Finder / File Explorer.
- project panel: new search in directory ( cmd-alt-shift-f|ctrl-alt-shift-f ) opens a project search scoped to the selected directory.
- project panel: remove from project removes a workspace root folder from the project.