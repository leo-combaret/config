#!/bin/zsh
set -euo pipefail

repo_dir="${0:A:h}"
timestamp="$(date +%Y%m%d%H%M%S)"

link_file() {
  local source="$1"
  local target="$2"
  local target_dir

  target_dir="$(dirname "$target")"
  mkdir -p "$target_dir"

  if [[ -L "$target" ]]; then
    rm "$target"
  elif [[ -e "$target" ]]; then
    mv "$target" "$target.backup.$timestamp"
  fi

  ln -s "$source" "$target"
}

chmod +x "$repo_dir/bin/zed-mistral-switch"
chmod +x "$repo_dir/zed/scripts/copy_selection_reference.py"
chmod +x "$repo_dir/../scripts/zellij/zed-open-zellij.sh"

link_file "$repo_dir/github/.gitconfig" "$HOME/.gitconfig"
link_file "$repo_dir/karabiner/karabiner.json" "$HOME/.config/karabiner/karabiner.json"
link_file "$repo_dir/zed/keymap.json" "$HOME/.config/zed/keymap.json"
link_file "$repo_dir/zed/settings.json" "$HOME/.config/zed/settings.json"
link_file "$repo_dir/zed/tasks.json" "$HOME/.config/zed/tasks.json"
link_file "$repo_dir/zed/scripts/copy_selection_reference.py" "$HOME/.config/zed/scripts/copy_selection_reference.py"
link_file "$repo_dir/zellij/config.kdl" "$HOME/.config/zellij/config.kdl"
link_file "$repo_dir/zellij/layouts/default.kdl" "$HOME/.config/zellij/layouts/default.kdl"
link_file "$repo_dir/bin/zed-mistral-switch" "$HOME/.local/bin/zed-mistral-switch"
link_file "$repo_dir/launch_agents/com.leocombaret.zed-project-overlay.plist" "$HOME/Library/LaunchAgents/com.leocombaret.zed-project-overlay.plist"

overlay_app="$HOME/.local/Applications/ZedProjectOverlay.app"
overlay_binary="$overlay_app/Contents/MacOS/zed-project-overlay"
overlay_info="$overlay_app/Contents/Info.plist"

mkdir -p "$overlay_app/Contents/MacOS"
cp "$repo_dir/apps/ZedProjectOverlay/Info.plist" "$overlay_info"

if [[ ! -x "$overlay_binary" || "${FORCE_REBUILD_OVERLAY:-0}" == "1" ]]; then
  if ! command -v swiftc >/dev/null 2>&1; then
    echo "swiftc is required to build the Zed project overlay" >&2
    exit 69
  fi

  swiftc "$repo_dir/overlay/ZedProjectOverlay.swift" -o "$overlay_binary"
  chmod +x "$overlay_binary"

  if command -v codesign >/dev/null 2>&1; then
    codesign --force --deep --sign - "$overlay_app" >/dev/null 2>&1 || true
  fi
fi

jq empty "$repo_dir/karabiner/karabiner.json"
zsh -n "$repo_dir/bin/zed-mistral-switch"
zsh -n "$repo_dir/../scripts/zellij/zed-open-zellij.sh"
zsh -n "$repo_dir/install.sh"
if command -v zellij >/dev/null 2>&1; then
  zellij setup --check >/dev/null
fi

if command -v launchctl >/dev/null 2>&1; then
  launchctl bootout "gui/$UID/com.leocombaret.zed-project-overlay" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$UID" "$HOME/Library/LaunchAgents/com.leocombaret.zed-project-overlay.plist" >/dev/null 2>&1 || true
  launchctl enable "gui/$UID/com.leocombaret.zed-project-overlay" >/dev/null 2>&1 || true
  launchctl kickstart -k "gui/$UID/com.leocombaret.zed-project-overlay" >/dev/null 2>&1 || true
fi

echo "Installed config symlinks from $repo_dir"
