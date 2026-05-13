#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


LOG_FILE = Path.home() / ".config" / "zed" / "logs" / "copy_selection_reference.log"


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as log_file:
            log_file.write(f"{line}\n")
    except OSError:
        pass


def line_for_offset(text, offset):
    return text.count("\n", 0, offset) + 1


def selected_line_count(selected_text):
    if not selected_text:
        return 1

    selected_without_trailing_newlines = selected_text.rstrip("\r\n")
    if not selected_without_trailing_newlines:
        return 1

    return selected_without_trailing_newlines.count("\n") + 1


def ranges_for_selection(file_text, selected_text):
    candidates = [selected_text]

    if "\n" in selected_text and "\r\n" in file_text and "\r\n" not in selected_text:
        candidates.append(selected_text.replace("\n", "\r\n"))

    if "\r\n" in selected_text:
        candidates.append(selected_text.replace("\r\n", "\n"))

    seen = set()
    ranges = []
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)

        search_from = 0
        while True:
            start = file_text.find(candidate, search_from)
            if start == -1:
                break

            end = start + len(candidate) - 1
            ranges.append((line_for_offset(file_text, start), line_for_offset(file_text, end)))
            search_from = start + 1

    return ranges


def closest_range(ranges, row):
    if row is None:
        return ranges[0]

    def distance(line_range):
        start, end = line_range
        if start <= row <= end:
            return 0
        if row < start:
            return start - row
        return row - end

    return min(ranges, key=distance)


def derive_line_range(file_path, selected_text, row):
    if selected_text and file_path:
        try:
            file_text = Path(file_path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            file_text = ""

        ranges = ranges_for_selection(file_text, selected_text)
        if ranges:
            return closest_range(ranges, row)

    current_line = max(row or 1, 1)
    line_count = selected_line_count(selected_text)
    return (max(current_line - line_count + 1, 1), current_line)


def copy_to_clipboard(text):
    clipboard_command = "/usr/bin/pbcopy" if Path("/usr/bin/pbcopy").exists() else shutil.which("pbcopy")
    if clipboard_command:
        try:
            subprocess.run([clipboard_command], input=text, text=True, check=True)
            return f"copied with {clipboard_command}"
        except subprocess.CalledProcessError as error:
            log(f"pbcopy failed with exit code {error.returncode}")

    osascript = "/usr/bin/osascript" if Path("/usr/bin/osascript").exists() else shutil.which("osascript")
    if osascript:
        try:
            subprocess.run(
                [osascript, "-e", "set the clipboard to (system attribute \"ZED_CLIPBOARD_TEXT\")"],
                env={**os.environ, "ZED_CLIPBOARD_TEXT": text},
                check=True,
            )
            return f"copied with {osascript}"
        except subprocess.CalledProcessError as error:
            log(f"osascript clipboard fallback failed with exit code {error.returncode}")

    raise RuntimeError("no working clipboard command found")


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("COPY_REF_FILE") or os.environ.get("ZED_FILE", "")
    relative_file = (
        sys.argv[2]
        if len(sys.argv) > 2
        else os.environ.get("COPY_REF_RELATIVE_FILE") or os.environ.get("ZED_RELATIVE_FILE", file_path)
    )
    row_text = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("COPY_REF_ROW") or os.environ.get("ZED_ROW", "")
    selected_text = (
        sys.argv[4]
        if len(sys.argv) > 4
        else os.environ.get("COPY_REF_SELECTED_TEXT") or os.environ.get("ZED_SELECTED_TEXT", "")
    )

    try:
        row = int(row_text)
    except (TypeError, ValueError):
        row = None

    log(
        "started "
        f"file={file_path or '<missing>'} "
        f"relative_file={relative_file or '<missing>'} "
        f"row={row_text or '<missing>'} "
        f"selected_chars={len(selected_text)} "
        f"zellij={os.environ.get('ZELLIJ', '<unset>')} "
        f"zellij_disable={os.environ.get('ZED_AUTO_ZELLIJ_DISABLE', '<unset>')} "
        f"shell={os.environ.get('SHELL', '<unset>')}"
    )

    try:
        start_line, end_line = derive_line_range(file_path, selected_text, row)
        message = f"at lines {start_line} to {end_line} in file {relative_file}"
        result = copy_to_clipboard(message)
    except Exception as error:
        log(f"ERROR {type(error).__name__}: {error}")
        return 1

    log(f"OK {result}: {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
