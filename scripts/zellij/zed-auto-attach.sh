# >>> zed zellij auto-attach >>>
_zed_auto_zellij_log() {
  local log_file="${HOME}/.config/zed/logs/zellij-auto-attach.log"
  mkdir -p "${log_file:h}" 2>/dev/null || return
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$log_file" 2>/dev/null
}

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

_zed_auto_zellij_session_is_exited() {
  local session="$1"
  "$zellij_bin" list-sessions --no-formatting 2>/dev/null |
    awk -v session="$session" '$1 == session && index($0, "(EXITED - attach to resurrect)") { found = 1 } END { exit found ? 0 : 1 }'
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
  if [[ -n "${ZELLIJ:-}" ]]; then
    return
  fi
  if [[ -n "${ZED_AUTO_ZELLIJ_DISABLE:-}" ]]; then
    _zed_auto_zellij_log "skip disabled pid=$$ pwd=$PWD"
    return
  fi
  if [[ -n "${ZED_FILE:-}${ZED_RELATIVE_FILE:-}${ZED_ROW:-}${ZED_SELECTED_TEXT:-}" ]]; then
    _zed_auto_zellij_log "skip zed-task-env pid=$$ pwd=$PWD zed_file=${ZED_FILE:-<unset>} zed_row=${ZED_ROW:-<unset>}"
    return
  fi

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
    if _zed_auto_zellij_session_is_exited "$session"; then
      _zed_auto_zellij_log "skip exited session=$session pid=$$ pwd=$PWD"
      ((index++))
      continue
    fi
    if ! _zed_auto_zellij_session_has_clients "$session"; then
      break
    fi
    ((index++))
  done

  _zed_auto_zellij_log "attach session=$session pid=$$ pwd=$PWD"
  "$zellij_bin" attach --create "$session"
}

_zed_auto_zellij
unset -f _zed_auto_zellij _zed_auto_zellij_log _zed_auto_zellij_from_zed _zed_auto_zellij_session_exists _zed_auto_zellij_session_is_exited _zed_auto_zellij_session_has_clients 2>/dev/null
# <<< zed zellij auto-attach <<<
