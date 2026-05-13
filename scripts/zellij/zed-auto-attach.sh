# >>> zed zellij auto-attach >>>
_zed_auto_zellij_from_zed() {
  [[ "${ZED_AUTO_ZELLIJ:-}" == "1" ]] && return 0

  local pid comm
  pid="$$"
  while [[ -n "$pid" && "$pid" != "0" ]]; do
    comm="$(ps -p "$pid" -o comm= 2>/dev/null)"
    if [[ "$comm" == *"/Zed.app/Contents/MacOS/zed"* || "${comm:t}" == "zed" ]]; then
      return 0
    fi
    pid="$(ps -p "$pid" -o ppid= 2>/dev/null | tr -d ' ')"
  done

  return 1
}

_zed_auto_zellij_session_exists() {
  local session="$1"
  "$zellij_bin" list-sessions --short 2>/dev/null | grep -Fxq -- "$session"
}

_zed_auto_zellij_session_has_clients() {
  local session="$1"
  "$zellij_bin" --session "$session" action list-clients 2>/dev/null |
    awk 'NR > 1 && NF { found = 1 } END { exit found ? 0 : 1 }'
}

_zed_auto_zellij() {
  [[ -o interactive ]] || return
  [[ -t 1 ]] || return
  _zed_auto_zellij_from_zed || return
  [[ -z "${ZELLIJ:-}" ]] || return
  [[ -z "${ZED_AUTO_ZELLIJ_DISABLE:-}" ]] || return

  local zellij_bin
  zellij_bin="$(command -v zellij 2>/dev/null)"
  [[ -n "$zellij_bin" ]] || zellij_bin="/opt/homebrew/bin/zellij"
  [[ -x "$zellij_bin" ]] || return

  local root base safe_base session index
  root="$(git rev-parse --show-toplevel 2>/dev/null || pwd -P)"
  [[ -n "$root" ]] || return

  base="${root:t}"
  [[ -n "$base" ]] || base="root"
  safe_base="$(printf '%s' "$base" | LC_ALL=C tr -c '[:alnum:]_.-' '_')"
  safe_base="${safe_base[1,48]}"

  index=1
  while true; do
    session="${safe_base}${index}"
    if ! _zed_auto_zellij_session_exists "$session"; then
      break
    fi
    if ! _zed_auto_zellij_session_has_clients "$session"; then
      break
    fi
    ((index++))
  done

  "$zellij_bin" attach --create "$session"
}

_zed_auto_zellij
unset -f _zed_auto_zellij _zed_auto_zellij_from_zed _zed_auto_zellij_session_exists _zed_auto_zellij_session_has_clients 2>/dev/null
# <<< zed zellij auto-attach <<<
