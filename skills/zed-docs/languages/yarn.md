# Yarn
Yarn is a JavaScript package manager that provides deterministic dependency resolution and offline caching.
## Setup
1. Run yarn dlx @yarnpkg/sdks base to generate a .yarn/sdks directory.
2. Set your language server (e.g. VTSLS) to use TypeScript SDK from .yarn/sdks/typescript/lib directory in LSP initialization options . The actual setting depends on your language server; for example, for VTSLS set typescript.tsdk .
After configuration, language server features (Go to Definition, completions, hover documentation) should work correctly.