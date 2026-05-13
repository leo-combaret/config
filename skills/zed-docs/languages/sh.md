# Shell Scripts
Shell Scripts (bash, zsh, dash, sh) are supported natively by Zed.
- Tree-sitter: tree-sitter/tree-sitter-bash
## Settings
Configure settings in Settings ( cmd-,|ctrl-, ) under Languages > Shell Script, or add to your settings file:
```
"languages": {
    "Shell Script": {
      "tab_size": 2,
      "hard_tabs": false
    }
  }
```
### Formatting
Zed supports auto-formatting Shell Scripts using external tools like shfmt .
1. Install shfmt :
```
brew install shfmt            # macos (homebrew)
sudo apt-get install shfmt    # debian/ubuntu
dnf install shfmt             # fedora
yum install shfmt             # redhat
pacman -Sy shfmt              # archlinux
choco install shfmt           # windows (chocolatey)
```
1. Ensure shfmt is available in your path and check the version:
```
which shfmt
shfmt --version
```
1. Configure formatting in Settings ( cmd-,|ctrl-, ) under Languages > Shell Script, or add to your settings file:
```
"languages": {
    "Shell Script": {
      "format_on_save": "on",
      "formatter": {
        "external": {
          "command": "shfmt",
          // Change `--indent 2` to match your preferred tab_size
          "arguments": ["--filename", "{buffer_path}", "--indent", "2"]
        }
      }
    }
  }
```
## See also:
- Zed Docs: Language Support: Bash
- Zed Docs: Language Support: Fish