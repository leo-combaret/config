# PowerShell
PowerShell language support in Zed is provided by the community-maintained Zed PowerShell extension . Please report issues to: github.com/wingyplus/zed-powershell/issues
- Tree-sitter: airbus-cert/tree-sitter-powershell
- Language Server: PowerShell/PowerShellEditorServices
## Setup
### Install PowerShell 7+
- macOS: brew install powershell/tap/powershell
- Alpine: Installing PowerShell on Alpine Linux
- Debian: Install PowerShell on Debian Linux
- RedHat: Install PowerShell on RHEL
- Ubuntu: Install PowerShell on RHEL
- Windows: Install PowerShell on Windows
The Zed PowerShell extension will default to the pwsh executable found in your path.
### Install PowerShell Editor Services (Optional)
The Zed PowerShell extensions will attempt to download PowerShell Editor Services automatically.
If want to use a specific binary, you can specify in your that in your Zed settings.json:
```
"lsp": {
    "powershell-es": {
      "binary": {
        "path": "/path/to/PowerShellEditorServices"
      }
    }
  }
```