# Jsonnet
Jsonnet language support in Zed is provided by the community-maintained Jsonnet extension .
- Tree-sitter: sourcegraph/tree-sitter-jsonnet
- Language Server: grafana/jsonnet-language-server
## Configuration
Workspace configuration options can be passed to the language server via the lsp settings of the settings.json .
The following example configures jsonnet-language-server to resolve tanka import paths:
```
{
  "lsp": {
    "jsonnet-language-server": {
      "settings": {
        "resolve_paths_with_tanka": true
      }
    }
  }
}
```