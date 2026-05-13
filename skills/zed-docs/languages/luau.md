# Luau
Luau is a fast, small, safe, gradually typed, embeddable scripting language derived from Lua. Luau was developed by Roblox and is available under the MIT license.
Luau language support in Zed is provided by the community-maintained Luau extension . Report issues to: https://github.com/4teapo/zed-luau/issues
- Tree-sitter: 4teapo/tree-sitter-luau
- Language Server: JohnnyMorganz/luau-lsp
## Configuration
Configuration instructions are available in the Luau Zed Extension README .
## Formatting
To support automatically formatting your code, you can use JohnnyMorganz/StyLua , a Lua code formatter.
Install with:
```
# macOS via Homebrew
brew install stylua
# Or via Cargo
cargo install stylua --features lua52,lua53,lua54,luau
```
Configure formatting in Settings ( cmd-,|ctrl-, ) under Languages > Luau, or add to your settings file:
```
"languages": {
    "Luau": {
      "formatter": {
        "external": {
          "command": "stylua",
          "arguments": ["-"]
        }
      }
    }
  }
```