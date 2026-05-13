# Plugin API
Please also see the Rust-specific documentation: zellij-tile .
The plugin API provides plugins with several capabilities:
- Events - A plugin can subscribe to one or more of these and receive an update whenever they happen.
- Commands - These are functions exported to the plugin, allowing it to affect Zellij and add functionality to it.
- Accessing the HD - A plugin can use its development language's own standard library to access the filesystem folder in which Zellij was opened.
- Workers for Async Tasks - A plugin can have multiple workers to which it can offload heavy or long-running tasks without blocking its own rendering.
- Log debug or error messages - A plugin can log messages to STDERR which will in the Zellij logs.