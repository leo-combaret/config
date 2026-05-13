---
name: zed-docs
description: "Documentation for zed.dev and the Zed code editor. Use when the user asks about Zed, zed.dev docs, installing or configuring Zed, AI features, Agent Panel, MCP, key bindings, debugger, tasks, terminal, Git, remote development, language support, extensions, settings, CLI, telemetry, or migration guides from https://zed.dev/docs."
---

# Zed Documentation

> 164 pages from [https://zed.dev/docs](https://zed.dev/docs)

## Overview

These docs cover Zed, an open-source code editor with built-in collaboration, AI-assisted editing, language tooling, debugging, tasks, terminal workflows, Git integration, remote development, and extension support. The crawl includes the mdBook sidebar: setup and platform guides, AI Agent Panel and MCP configuration, editing and navigation workflows, per-language setup notes, extension authoring, migration guides, account/privacy topics, reference pages for settings/actions/CLI, and development notes for building Zed itself.

Use this skill to answer practical Zed questions by opening the most relevant local markdown file below, then read adjacent files when a workflow spans multiple areas such as AI provider setup plus tool permissions, language setup plus debugging, or extension development plus publishing.

## Contents

### Welcome

- [Getting Started](getting-started.md)
- [Installing Zed](installation.md)
- [Update Zed](update.md)
- [Uninstall](uninstall.md)
- [Troubleshooting](troubleshooting.md)

### AI

- [AI](ai/overview.md)
- [Agent Panel](ai/agent-panel.md)
- [Tools](ai/tools.md)
- [Tool Permissions](ai/tool-permissions.md)
- [External Agents](ai/external-agents.md)
- [Parallel Agents](ai/parallel-agents.md)
- [Inline Assistant](ai/inline-assistant.md)
- [Edit Prediction](ai/edit-prediction.md)
- [Using Rules](ai/rules.md)
- [Model Context Protocol](ai/mcp.md)
- [Configuration](ai/configuration.md)
- [LLM Providers](ai/llm-providers.md)
- [Agent Settings](ai/agent-settings.md)
- [Subscription](ai/subscription.md)
- [Models](ai/models.md)
- [Plans and Usage](ai/plans-and-usage.md)
- [Billing](ai/billing.md)

### Working With Code

- [Editing Code](editing-code.md)
- [Completions](completions.md)
- [Snippets](snippets.md)
- [Diagnostics](diagnostics.md)
- [Multibuffers](multibuffers.md)
- [Finding & Navigating](finding-navigating.md)
- [Command Palette](command-palette.md)
- [Outline Panel](outline-panel.md)
- [Project Panel](project-panel.md)
- [Tab Switcher](tab-switcher.md)
- [Running & Testing](running-testing.md)
- [Terminal](terminal.md)
- [Tasks](tasks.md)
- [Debugger](debugger.md)
- [REPL](repl.md)
- [Git](git.md)
- [Modelines](modelines.md)

### Collaboration

- [Collaboration](collaboration/overview.md)
- [Channels](collaboration/channels.md)
- [Contacts and Private Calls](collaboration/contacts-and-private-calls.md)

### Remote Development

- [Remote Development](remote-development.md)
- [Environment Variables](environment.md)
- [Dev Containers](dev-containers.md)

### Platform Support

- [Zed on macOS](macos.md)
- [Zed on Windows](windows.md)
- [Zed on Linux](linux.md)

### Customization

- [Appearance](appearance.md)
- [Themes](themes.md)
- [Icon Themes](icon-themes.md)
- [Visual Customization](visual-customization.md)
- [Key bindings](key-bindings.md)
- [Vim Mode](vim.md)
- [Helix Mode](helix.md)

### Language Support

- [Language Support in Zed](languages.md)
- [Configuring Supported Languages](configuring-languages.md)
- [Toolchains](toolchains.md)
- [Semantic Tokens](semantic-tokens.md)

#### Per-Language Guides

- [Ansible](languages/ansible.md)
- [AsciiDoc](languages/asciidoc.md)
- [Astro](languages/astro.md)
- [Bash](languages/bash.md)
- [Biome](languages/biome.md)
- [C](languages/c.md)
- [C++](languages/cpp.md)
- [C#](languages/csharp.md)
- [Clojure](languages/clojure.md)
- [CSS](languages/css.md)
- [Dart](languages/dart.md)
- [Deno](languages/deno.md)
- [Diff](languages/diff.md)
- [Docker](languages/docker.md)
- [Elixir](languages/elixir.md)
- [Elm](languages/elm.md)
- [Emmet](languages/emmet.md)
- [Erlang](languages/erlang.md)
- [Fish](languages/fish.md)
- [GDScript](languages/gdscript.md)
- [Gleam](languages/gleam.md)
- [GLSL](languages/glsl.md)
- [Go](languages/go.md)
- [Groovy](languages/groovy.md)
- [Haskell](languages/haskell.md)
- [Helm](languages/helm.md)
- [HTML](languages/html.md)
- [Java](languages/java.md)
- [JavaScript](languages/javascript.md)
- [Julia](languages/julia.md)
- [JSON](languages/json.md)
- [Jsonnet](languages/jsonnet.md)
- [Kotlin](languages/kotlin.md)
- [Lua](languages/lua.md)
- [Luau](languages/luau.md)
- [Makefile](languages/makefile.md)
- [Markdown](languages/markdown.md)
- [Nim](languages/nim.md)
- [OCaml](languages/ocaml.md)
- [OpenTofu](languages/opentofu.md)
- [PHP](languages/php.md)
- [PowerShell](languages/powershell.md)
- [Prisma](languages/prisma.md)
- [Proto](languages/proto.md)
- [PureScript](languages/purescript.md)
- [How to Set Up Python in Zed](languages/python.md)
- [R](languages/r.md)
- [Rego](languages/rego.md)
- [ReStructuredText (rst)](languages/rst.md)
- [Racket](languages/racket.md)
- [Roc](languages/roc.md)
- [Ruby](languages/ruby.md)
- [Rust](languages/rust.md)
- [Scala](languages/scala.md)
- [Scheme](languages/scheme.md)
- [Shell Scripts](languages/sh.md)
- [SQL](languages/sql.md)
- [Svelte](languages/svelte.md)
- [Swift](languages/swift.md)
- [Tailwind CSS](languages/tailwindcss.md)
- [Terraform](languages/terraform.md)
- [TOML](languages/toml.md)
- [TypeScript](languages/typescript.md)
- [Uiua](languages/uiua.md)
- [Vue](languages/vue.md)
- [XML](languages/xml.md)
- [YAML](languages/yaml.md)
- [Yara](languages/yara.md)
- [Yarn](languages/yarn.md)
- [Zig](languages/zig.md)

### Extensions

- [Extensions](extensions.md)
- [Installing Extensions](extensions/installing-extensions.md)
- [Developing Extensions](extensions/developing-extensions.md)
- [Extension Capabilities](extensions/capabilities.md)
- [Language Extensions](extensions/languages.md)
- [Debugger Extensions](extensions/debugger-extensions.md)
- [Themes](extensions/themes.md)
- [Icon Themes](extensions/icon-themes.md)
- [Snippets](extensions/snippets.md)
- [Agent Server Extensions](extensions/agent-servers.md)
- [MCP Server Extensions](extensions/mcp-extensions.md)

### Coming From

- [How to Migrate from VS Code to Zed](migrate/vs-code.md)
- [How to Migrate from IntelliJ IDEA to Zed](migrate/intellij.md)
- [How to Migrate from PyCharm to Zed](migrate/pycharm.md)
- [How to Migrate from WebStorm to Zed](migrate/webstorm.md)
- [How to Migrate from RustRover to Zed](migrate/rustrover.md)

### Reference

- [All Settings](reference/all-settings.md)
- [All Actions](all-actions.md)
- [CLI Reference](reference/cli.md)

### Account & Privacy

- [Authenticate with Zed](authentication.md)
- [Roles](roles.md)
- [Privacy and Security](ai/privacy-and-security.md)
- [Zed and trusted worktrees](worktree-trust.md)
- [Zed AI Features and Privacy](ai/ai-improvement.md)
- [Telemetry in Zed](telemetry.md)

### Developing Zed

- [Developing Zed](development.md)
- [Rough quick CPU profiling (Flamechart)](performance.md)

#### Build, Debugging, and Release Notes

- [Building Zed for macOS](development/macos.md)
- [Building Zed for Linux](development/linux.md)
- [Building Zed for Windows](development/windows.md)
- [Building Zed for FreeBSD](development/freebsd.md)
- [Using a debugger](development/debuggers.md)
- [Zed Development: Glossary](development/glossary.md)
- [Release Notes](development/release-notes.md)
- [Debugging Crashes](development/debugging-crashes.md)

## Lookup

1. Find the relevant section in Contents above
2. Read that file with the Read tool
3. If the answer spans sections, read multiple files
