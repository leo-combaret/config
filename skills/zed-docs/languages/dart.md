# Dart
Dart support is available through the Dart extension .
- Tree-sitter: UserNobody14/tree-sitter-dart
- Language Server: dart language-server
## Pre-requisites
You will need to install the Dart SDK.
You can install dart from dart.dev/get-dart or via the Flutter Version Management CLI (fvm)
## Configuration
The dart extension requires no configuration if you have dart in your path:
```
which dart
dart --version
```
If you would like to use a specific dart binary or use dart via FVM you can specify the dart binary in your Zed settings.jsons file:
```
{
  "lsp": {
    "dart": {
      "binary": {
        "path": "/opt/homebrew/bin/fvm",
        "arguments": ["dart", "language-server", "--protocol=lsp"]
      }
    }
  }
}
```
### Formatting
Dart by-default uses a very conservative maximum line length (80). If you would like the dart LSP to permit a longer line length when auto-formatting, add the following to your Zed settings.json:
```
{
  "lsp": {
    "dart": {
      "settings": {
        "lineLength": 140
      }
    }
  }
}
```
Please see the Dart documentation for more information on dart language-server capabilities .