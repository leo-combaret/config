# OpenTofu
OpenTofu support is available through the OpenTofu extension .
- Tree-sitter: MichaHoffmann/tree-sitter-hcl
- Language Server: opentofu/tofu-ls
## Configuration
To automatically use the OpenTofu extension and language server when editing .tf and .tfvars files, either uninstall the Terraform extension or add this to your settings.json:
```
"file_types": {
  "OpenTofu": ["tf"],
  "OpenTofu Vars": ["tfvars"]
},
```
See the full list of server settings here .