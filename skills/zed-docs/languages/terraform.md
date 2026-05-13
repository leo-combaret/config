# Terraform
Terraform support is available through the Terraform extension .
- Tree-sitter: MichaHoffmann/tree-sitter-hcl
- Language Server: hashicorp/terraform-ls
## Configuration
The Terraform language server can be configured in your settings.json , e.g.:
```
{
  "lsp": {
    "terraform-ls": {
      "initialization_options": {
        "experimentalFeatures": {
          "prefillRequiredFields": true
        }
      }
    }
  }
}
```
See the full list of server settings here .