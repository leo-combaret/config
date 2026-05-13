# Personal Config

This repo stores the local keyboard/editor setup for this machine.

## Contents

- `karabiner/karabiner.json`: Karabiner-Elements rules.
- `github/.gitconfig`: Git aliases and identity.
- `zed/keymap.json`: Zed key bindings.
- `zed/settings.json`: Zed editor and terminal settings.
- `zed/tasks.json`: Zed task definitions.
- `zed/scripts/copy_selection_reference.py`: helper for copying a selected line reference.
- `zellij/config.kdl`: Zellij keybindings and pane behavior.
- `zellij/layouts/default.kdl`: default Zellij pane layout.
- `../scripts/zellij/zed-open-zellij.sh`: helper used by the Zed terminal task.
- `bin/zed-mistral-switch`: helper used by Karabiner to focus Mistral Zed worktrees.
- `apps/ZedProjectOverlay/Info.plist`: app bundle metadata for the overlay helper.
- `overlay/ZedProjectOverlay.swift`: native overlay shown on matching Zed worktree windows.
- `launch_agents/com.leocombaret.zed-project-overlay.plist`: starts the overlay at login.

## Current Shortcuts

- Tap left Command in Zed: sends `F18`, which Zed maps in `zed/keymap.json`.
- Right Command + `1`: open/focus `~/mistral/dashboard` in Zed.
- Right Command + `2`: open/focus `~/mistral/seattle` in Zed.
- Right Command + `3`: open/focus `~/mistral/budapest` in Zed.
- Right Command + `4`: open/focus `~/mistral/dakar` in Zed.
- Matching frontmost Zed worktree windows show a top-center overlay in this order: `dashboard`, `seattle`, `budapest`, `dakar`.

## Install

From this directory: asd;lkfj

```sh
./install.sh
```

The installer symlinks the tracked files into:

- `~/.config/karabiner/karabiner.json`
- `~/.gitconfig`
- `~/.config/zed/keymap.json`
- `~/.config/zed/settings.json`
- `~/.config/zed/tasks.json`
- `~/.config/zed/scripts/copy_selection_reference.py`
- `~/.config/zellij/config.kdl`
- `~/.config/zellij/layouts/default.kdl`
- `~/.local/bin/zed-mistral-switch`
- `~/Library/LaunchAgents/com.leocombaret.zed-project-overlay.plist`

It also compiles `overlay/ZedProjectOverlay.swift` into `~/.local/Applications/ZedProjectOverlay.app` and starts the launch agent.

The overlay requires Accessibility permission because it reads Zed's front window title, document path, and frame. If macOS prompts, approve `ZedProjectOverlay` in System Settings > Privacy & Security > Accessibility.

To rebuild the overlay binary after changing `overlay/ZedProjectOverlay.swift`, run:

```sh
FORCE_REBUILD_OVERLAY=1 ./install.sh
```

Rebuilding changes the app's local code identity, so macOS may require toggling the `ZedProjectOverlay` Accessibility permission off and on again.

If a real file already exists at one of those paths, the installer moves it aside with a timestamped `.backup.*` suffix.
