# Bash
Bash support is available through the Bash extension .
- Tree-sitter: tree-sitter/tree-sitter-bash
- Language Server: bash-lsp/bash-language-server
## Configuration
When shellcheck is available bash-language-server will use it internally to provide diagnostics.
### Install shellcheck :
```
brew install shellcheck             # macOS (HomeBrew)
apt-get install shellcheck          # Ubuntu/Debian
pacman -S shellcheck                # ArchLinux
dnf install shellcheck              # Fedora
yum install shellcheck              # CentOS/RHEL
zypper install shellcheck           # openSUSE
choco install shellcheck            # Windows (Chocolatey)
```
And verify it is available from your path:
```
which shellcheck
shellcheck --version
```
If you wish to customize the warnings/errors reported you just need to create a .shellcheckrc file. You can do this in the root of your project or in your home directory ( ~/.shellcheckrc ). See: shellcheck documentation for more.
### See also:
- Zed Docs: Language Support: Shell Scripts