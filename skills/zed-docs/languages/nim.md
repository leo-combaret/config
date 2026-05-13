# Nim
Nim language support in Zed is provided by the community-maintained Nim extension . Report issues to: https://github.com/foxoman/zed-nim/issues
- Tree-sitter: alaviss/tree-sitter-nim
- Language Server: nim-lang/langserver
## Formatting
To use arnetheduck/nph as a formatter, follow the nph installation instructions .
Configure formatting in Settings ( cmd-,|ctrl-, ) under Languages > Nim, or add to your settings file:
```
"languages": {
    "Nim": {
      "formatter": {
        "external": {
          "command": "nph",
          "arguments": ["-"]
        }
      }
    }
  }
```