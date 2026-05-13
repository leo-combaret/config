# Haskell
Haskell support is available through the Haskell extension .
- Tree-sitter: tree-sitter-haskell
- Language Server: haskell-language-server
## Installing HLS
Recommended method to install haskell-language-server (HLS) is via ghcup ( curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh ):
```
ghcup install hls
which haskell-language-server-wrapper
```
## Configuring HLS
If you need to configure haskell-language-server (hls) you can add configuration options to your Zed settings.json:
```
{
  "lsp": {
    "hls": {
      "initialization_options": {
        "haskell": {
          "formattingProvider": "fourmolu"
        }
      }
    }
  }
}
```
See the official configuring haskell-language-server docs for more options.
If you would like to use a specific hls binary, or perhaps use static-ls as a drop-in replacement instead, you can specify the binary path and arguments:
```
{
  "lsp": {
    "hls": {
      "binary": {
        "path": "static-ls",
        "arguments": ["--experimentalFeatures"]
      }
    }
  }
}
```