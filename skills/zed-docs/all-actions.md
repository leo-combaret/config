# All Actions
NOTE: This does not wait for asynchronous actions to complete before running the next action. Keymap Name: action::Sequence
Does not apply to platform menu bars (e.g. on macOS). Keymap Name: app_menu::ActivateMenuLeft
Does not apply to platform menu bars (e.g. on macOS). Keymap Name: app_menu::ActivateMenuRight
Does not apply to platform menu bars (e.g. on macOS). Keymap Name: app_menu::OpenApplicationMenu
Use collab_panel::OpenSelectedChannelNotes to open the channel notes for the selected channel in the collab panel.
If you want to open a specific channel, use zed::OpenZedUrl with a channel notes URL - can be copied via "Copy link to section" in the context menu of the channel notes buffer. These URLs look like https://zed.dev/channel/channel-name-CHANNEL_ID/notes . Keymap Name: collab::OpenChannelNotes
Use collab::OpenChannelNotes to open the channel notes for the current call. Keymap Name: collab_panel::OpenSelectedChannelNotes
This action is only available when the active formatter can format ranges. When using a language server, this sends an LSP range formatting request for each selection, and is hidden when the selected buffer's configured language server does not advertise range-formatting support. When using Prettier, Prettier's own range formatting is used to format the encompassing range of all selections, and resulting edits outside the selected ranges are discarded. External command formatters do not support range formatting and are skipped. Keymap Name: editor::FormatSelections
In keymap JSON this is written as:
["zed::Unbind", "editor::NewLine"] Keymap Name: zed::Unbind