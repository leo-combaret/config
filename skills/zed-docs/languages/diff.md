# Diff
Diff support is available natively in Zed.
- Tree-sitter: zed-industries/the-mikedavis/tree-sitter-diff
## Configuration
Zed will not attempt to format diff files and has remove_trailing_whitespace_on_save and ensure-final-newline-on-save set to false.
Zed will automatically recognize files with patch and diff extensions as Diff files. To recognize other extensions, add them to file_types in your Zed settings.json:
```
"file_types": {
    "Diff": ["dif"]
  },
```