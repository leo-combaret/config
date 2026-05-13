# Options
Configuration options can be set directly at the root of the configuration file
These include:
- on_force_close
- simplified_ui
- default_shell
- pane_frames
- theme
- theme_dark
- theme_light
- default_layout
- default_mode
- mouse_mode
- scroll_buffer_size
- copy_command
- copy_clipboard
- copy_on_select
- scrollback_editor
- mirror_session
- layout_dir
- theme_dir
- env
- rounded_corners
- hide_session_name
- auto_layout
- styled_underlines
- session_serialization
- pane_viewport_serialization
- scrollback_lines_to_serialize
- serialization_interval
- disable_session_metadata
- stacked_resize
- show_startup_tips
- show_release_notes
- post_command_discovery_hook
- web_server
- web_server_ip
- web_server_port
- web_server_cert
- web_server_key
- enforce_https_on_localhost
- base_url
- web_client
- advanced_mouse_actions
- default_cwd
- osc8_hyperlinks
- session_name
- attach_to_session
- support_kitty_keyboard_protocol
- web_sharing
- mouse_hover_effects
- visual_bell
- focus_follows_mouse
- mouse_click_through
### on_force_close
Choose what to do when zellij receives SIGTERM, SIGINT, SIGQUIT or SIGHUP eg. when terminal window with an active zellij session is closed
Options:
- detach (Default)
- quit
```
on_force_close "quit"
```
### simplified_ui
Send a request for a simplified ui (without arrow fonts) to plugins
Options:
- true
- false (Default)
```
simplified_ui true
```
### default_shell
Choose the path to the default shell that zellij will use for opening new panes
Default: $SHELL
```
default_shell "fish"
```
### pane_frames
Toggle between having pane frames around the panes
Options:
- true (default)
- false
```
pane_frames true
```
### theme
Choose the Zellij color theme. This theme must be specified in the themes section or loaded from the themes folder. See themes
Default: default
```
theme "default"
```
### theme_dark
Name of the theme to use as the "dark" theme. Used by the SetDarkTheme / ToggleTheme actions, and applied automatically when the host terminal reports it is in dark mode (CSI 2031 / DSR 997). The named theme must be specified in the themes section or loaded from the themes folder. See themes
```
theme_dark "catppuccin-mocha"
```
### theme_light
Name of the theme to use as the "light" theme. Used by the SetLightTheme / ToggleTheme actions, and applied automatically when the host terminal reports it is in light mode (CSI 2031 / DSR 997). The named theme must be specified in the themes section or loaded from the themes folder. See themes
```
theme_light "catppuccin-latte"
```
### default_layout
The name of the layout to load on startup (must be in the layouts folder). See layouts
Default: "default"
```
default_layout "compact"
```
### default_mode "locked"
Choose the mode that zellij uses when starting up.
Default: normal
```
default_mode "locked"
```
### mouse_mode
Toggle enabling the mouse mode. On certain configurations, or terminals this could potentially interfere with copying text.
Options:
- true (default)
- false
```
mouse_mode false
```
### scroll_buffer_size
Configure the scroll back buffer size This is the number of lines zellij stores for each pane in the scroll back buffer. Excess number of lines are discarded in a FIFO fashion.
Valid values: positive integers
Default value: 10000
```
scroll_buffer_size 10000
```
### copy_command
Provide a command to execute when copying text. The text will be piped to the stdin of the program to perform the copy. This can be used with terminal emulators which do not support the OSC 52 ANSI control sequence that will be used by default if this option is not set.
Examples:
```
copy_command "xclip -selection clipboard" // x11
copy_command "wl-copy"                    // wayland
copy_command "pbcopy"                     // osx
```
### copy_clipboard
Choose the destination for copied text Allows using the primary selection buffer (on x11/wayland) instead of the system clipboard. Does not apply when using copy_command.
Options:
- system (default)
- primary
```
copy_clipboard "primary"
```
### copy_on_select
Enable or disable automatic copy of selection when releasing mouse
Default: true
```
copy_on_select false
```
### scrollback_editor
Path to the default editor to use to edit pane scrollbuffer as well as the CLI and layout edit commands
Default: $EDITOR or $VISUAL
```
scrollback_editor "/usr/bin/vim"
```
### mirror_session
When attaching to an existing session with other users, should the session be mirrored (true) or should each user have their own cursor (false) Default: false
```
mirror_session true
```
### layout_dir
The folder in which Zellij will look for layouts
```
layout_dir "/path/to/my/layout_dir"
```
### theme_dir
The folder in which Zellij will look for themes
```
theme_dir "/path/to/my/theme_dir"
```
### env
A key -> value map of environment variables that will be set for each terminal pane Zellij starts.
```
env {
    RUST_BACKTRACE 1
    FOO "bar"
}
```
### rounded_corners
Set whether the pane frames (if visible) should have rounded corners.
This config variable is set differently than others:
```
ui {
    pane_frames {
        rounded_corners true
    }
}
```
### hide_session_name
Hides the session name (randomly generated or otherwise) from the UI
```
ui {
    pane_frames {
        hide_session_name true
    }
}
```
### auto_layout
Toggle between having Zellij lay out panes according to a predefined set of layouts whenever possible Options:
- true (default)
- false
```
auto_layout true
```
### styled_underlines
Toggle between supporting the extended "styled_underlines" ANSI protocol and ignoring it (can sometimes cause some issues in unsupported terminals). Options:
- true (default)
- false
```
styled_underlines true
```
### session_serialization
If enabled, sessions will be serialized to the cache folder (and thus become resurrectable between reboots or on exit). Read more about session resurrection . Options:
- true (default)
- false
```
session_serialization true
```
### pane_viewport_serialization
If enabled along with session_serialization , the pane viewport (the visible part of the terminal excluding the scrollback) will be serialized and resurrectable as well. Read more about session resurrection . Options:
- true
- false (default)
```
pane_viewport_serialization true
```
### scrollback_lines_to_serialize
When pane_viewport_serialization is enabled, setting scrollback_lines_to_serialize to 0 in the will serialize all scrollback and to any other number will serialize line number up to that scrollback. Read more about session resurrection .
Note: this might incur higher resource utilization (and certainly a higher cache folder usage...)
Options:
- 0 : serialize all scrollback
- int : serialize this much lines for each pane (max is the scrollback limit)
```
pane_viewport_serialization 100
```
### serialization_interval
How often in seconds sessions are serialized to disk (if session_serialization is enabled).
Note: this might incur higher resource utilization (and certainly a higher cache folder usage...)
Options:
- int : the interval in seconds
```
serialization_interval 60
```
### disable_session_metadata
Enable or disable writing of session metadata to disk
Note: If disabled, other sessions might not know metadata info on this session, so features such as the session-manager and session listing might not work properly.
Options:
- true
- false (default)
```
disable_session_metadata true
```
### stacked_resize
Attempt to stack panes with their neighbors when resizing non-directionally (by default Alt+/- ).
Options:
- true (default)
- false
```
stacked_resize true
```
### show_startup_tips
Show usage tips on Zellij startup. These can also be browsed through the about plugin with Ctrl o + a and then ? .
Options:
- true (default)
- false
```
show_startup_tips true
```
### show_release_notes
Show release notes on first run of a new version. These can also be browsed through the about plugin with Ctrl o + a .
Options:
- true (default)
- false
```
show_release_notes true
```
### post_command_discovery_hook
When Zellij attempts to discover commands running inside panes so that it can serialize them, it can sometimes be inaccurate. This can happen when (for example) commands are run inside some sort of wrapper. To get around this, it's possible to define a post_command_discovery_hook . This is a command that will run in the context of te user's default shell and be provided the $RESURRECT_COMMAND that has just been discovered for a specific pane and not yet serialized. Whatever this command sends over STDOUT will be serialized in place of the discovered command.
Example:
```
post_command_discovery_hook "echo \"$RESURRECT_COMMAND\" | sed 's/^sudo\\s\\+//'" // strip sudo from commands
```
### web_server
Whether to start the Zellij web-server on startup.
Options:
- true
- false (default)
### web_server_ip
The IP for the Zellij web-server to listen on when it's started. Default: 127.0.0.1 .
### web_server_port
The port for the Zellij web-server to listen on when it's started. Default: 8082 .
### web_server_cert
The path to the SSL certificate for the Zellij web-server . Note: the web_server_key must also be present for the server to serve itself as HTTPS.
### web_server_key
The path to the private_key of te SSL certificate for the Zellij web-server . Note: the web_server_cert must also be present for the server to serve itself as HTTPS.
### enforce_https_on_localhost
Whether to enforce https on localhost for the Zellij web-server . This is always enforced when listening on non-localhost addresses.
### base_url
Set the base URL path for the Zellij web-server . When set, the web server serves all content under this path prefix. This is useful when running behind a reverse proxy that serves Zellij under a subpath.
Default: none (served at root "/")
```
web_client {
    base_url "/zellij"
}
```
### web_client
Configuration having to do with the in-browser terminal of the Zellij web client (eg. colors, font). For more info, please see: web-server .
Options: - true - false (default)
### advanced_mouse_actions
Whether to enable mouse hover effects, multiple select functionality (pane grouping), and mouse-based pane resizing.
When enabled, the following mouse interactions are available:
- Drag tiled pane borders : Click and drag the border between tiled panes to resize them
- Ctrl+Drag floating pane borders : Hold Ctrl and drag the border of a floating pane to resize it
- Ctrl+ScrollWheel : Hold Ctrl and scroll the mouse wheel up or down to resize the focused pane (increases/decreases size by approximately 5 cells)
These interactions are shown as help text in the pane frame when hovering near resizable borders.
Options: - true (default) - false
### default_cwd
Set the default current working directory for new panes. When set, new panes will open in this directory unless otherwise specified.
```
default_cwd "/home/user/projects"
```
### osc8_hyperlinks
Enable clickable OSC8 hyperlink output in terminal panes. When enabled, programs that emit OSC8 escape sequences will produce clickable hyperlinks.
Options:
- true
- false (default)
```
osc8_hyperlinks true
```
### session_name
Set the name of the session to create when starting Zellij. If not set, a random name will be generated.
```
session_name "my-session"
```
### attach_to_session
If a session with the name specified in session_name already exists, attach to it instead of creating a new one.
Options:
- true
- false (default)
```
attach_to_session true
```
### support_kitty_keyboard_protocol
Enable support for the Kitty keyboard protocol. This allows for more detailed key reporting from the terminal. Defaults to true if the terminal supports it.
Options:
- true (default if terminal supports it)
- false
```
support_kitty_keyboard_protocol true
```
### web_sharing
Whether new sessions are shared through the local web server. This is separate from web_server which controls whether the server starts at all.
Options:
- "on" - new sessions are shared by default
- "off" - new sessions are not shared by default (Default)
- "disabled" - sharing is completely disabled
```
web_sharing "on"
```
### mouse_hover_effects
Enable mouse hover visual effects, such as pane frame highlight and help text when hovering over panes.
Options:
- true (default)
- false
```
mouse_hover_effects false
```
### visual_bell
Show visual bell indicators when a pane sends a bell character. This manifests as a brief pane/tab frame flash and a [!] suffix on the tab name.
Options:
- true (default)
- false
```
visual_bell false
```
### focus_follows_mouse
Whether to automatically focus panes when hovering over them with the mouse.
Options:
- true
- false (default)
```
focus_follows_mouse true
```
### mouse_click_through
Whether clicking a pane to focus it also sends the click event into the pane (to the running program). When false, the first click only focuses the pane and is consumed by Zellij.
Options:
- true
- false (default)
```
mouse_click_through true
```