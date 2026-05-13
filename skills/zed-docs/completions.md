# Completions
Zed supports two sources for completions:
1. "Code Completions" provided by Language Servers (LSPs) automatically installed by Zed or via Zed Language Extensions .
2. "Edit Predictions" provided by Zed's own Zeta model or by external providers like GitHub Copilot .
## Language Server Code Completions
When there is an appropriate language server available, Zed will provide completions of variable names, functions, and other symbols in the current file. You can disable these by adding the following to your Zed settings.json file:
```
"show_completions_on_input": false
```
You can manually trigger completions with ctrl-space or by triggering the editor::ShowCompletions action from the command palette.
> Note: Using
> ctrl-space
> in Zed requires disabling the macOS global shortcut.
> Open
> System Settings
> >
> Keyboard
> >
> Keyboard Shortcut
> s >
> Input Sources
> and uncheck
> Select the previous input source
> .
For more information, see:
- Configuring Supported Languages
- List of Zed Supported Languages
## Edit Predictions
Zed has built-in support for predicting multiple edits at a time via Zeta , Zed's open-source and open-data model. Edit predictions appear as you type, and most of the time, you can accept them by pressing tab .
See the edit predictions documentation for more information on how to setup and configure Zed's edit predictions.