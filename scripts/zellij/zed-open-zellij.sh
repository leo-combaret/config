#!/bin/zsh
set -e

zellij_bin="$(command -v zellij 2>/dev/null || true)"
[[ -n "$zellij_bin" ]] || zellij_bin="/opt/homebrew/bin/zellij"
[[ -x "$zellij_bin" ]] || {
  echo "zellij not found" >&2
  exit 1
}

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd -P)"
base="${root:t}"
[[ -n "$base" ]] || base="root"
safe_base="$(printf '%s' "$base" | LC_ALL=C tr -c '[:alnum:]_.-' '_')"
safe_base="${safe_base[1,48]}"

index=1
while true; do
  session="${safe_base}${index}"
  if ! "$zellij_bin" list-sessions --short 2>/dev/null | grep -Fxq -- "$session"; then
    break
  fi
  if ! "$zellij_bin" --session "$session" action list-clients 2>/dev/null |
    awk 'NR > 1 && NF { found = 1 } END { exit found ? 0 : 1 }'; then
    break
  fi
  ((index++))
done

exec "$zellij_bin" attach --create "$session"
