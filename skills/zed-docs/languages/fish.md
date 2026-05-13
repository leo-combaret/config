# Fish
Fish language support in Zed is provided by the community-maintained Fish extension . Report issues to: https://github.com/hasit/zed-fish/issues
- Tree-sitter: ram02z/tree-sitter-fish
### Formatting
Zed supports auto-formatting fish code using external tools like fish_indent , which is included with fish.
1. Ensure fish_indent is available in your path and check the version:
```
which fish_indent
fish_indent --version
```
1. Configure Zed to automatically format fish code with fish_indent :
```
"languages": {
    "Fish": {
      "formatter": {
        "external": {
          "command": "fish_indent"
        }
      }
    }
  },
```