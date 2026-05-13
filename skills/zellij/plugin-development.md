# Developing a Plugin
This section talks about developing a Zellij plugin in Rust.
- Development Environment : walks through the example Rust plugin, this will explain how to create a local environment to iterate over plugin development.
- Plugin Lifecycle : talks about the plugin interface and zellij-tile - the Rust library Zellij provides to facilitate development
- Rendering a UI : Talks about the implicit contracts Zellij has with plugins in regards to ANSI rendering
- Upgrading and Backwards Compatibility : Gives instructions on how to upgrade Zellij plugins when a new Zellij version comes out, and when this needs to be done