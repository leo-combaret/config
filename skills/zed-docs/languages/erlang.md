# Erlang
Erlang support is available through the Erlang extension .
- Tree-sitter: WhatsApp/tree-sitter-erlang
- Language Servers: erlang-ls/erlang_ls WhatsApp/erlang-language-platform
## Choosing a language server
The Erlang extension offers language server support for erlang_ls and erlang-language-platform .
erlang_ls is enabled by default.
Configure language servers in Settings ( cmd-,|ctrl-, ) under Languages > Erlang, or add to your settings file:
```
{
  "languages": {
    "Erlang": {
      "language_servers": ["elp", "!erlang-ls", "..."]
    }
  }
}
```
## See also:
- Elixir
- Gleam