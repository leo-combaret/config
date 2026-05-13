# Deno
Deno support is available through the Deno extension .
- Language server: Deno Language Server
## Deno Configuration
To use the Deno Language Server with TypeScript and TSX files, you will likely wish to disable the default language servers and enable Deno.
Configure language servers and formatters in Settings ( cmd-,|ctrl-, ) under Languages > JavaScript/TypeScript/TSX, or add to your settings file:
```
{
  "lsp": {
    "deno": {
      "settings": {
        "deno": {
          "enable": true
        }
      }
    }
  },
  "languages": {
    "JavaScript": {
      "language_servers": [
        "deno",
        "!typescript-language-server",
        "!vtsls",
        "!eslint"
      ],
      "formatter": "language_server"
    },
    "TypeScript": {
      "language_servers": [
        "deno",
        "!typescript-language-server",
        "!vtsls",
        "!eslint"
      ],
      "formatter": "language_server"
    },
    "TSX": {
      "language_servers": [
        "deno",
        "!typescript-language-server",
        "!vtsls",
        "!eslint"
      ],
      "formatter": "language_server"
    }
  }
}
```
See Configuring supported languages in the Zed documentation for more information.
## Configuration completion
To get completions for deno.json or package.json , add the following to your settings file ( how to edit ). For more details, see JSON .
```
"lsp": {
    "json-language-server": {
      "settings": {
        "json": {
          "schemas": [
            {
              "fileMatch": [
                "deno.json",
                "deno.jsonc"
              ],
              "url": "https://raw.githubusercontent.com/denoland/deno/refs/heads/main/cli/schemas/config-file.v1.json"
            },
            {
              "fileMatch": [
                "package.json"
              ],
              "url": "https://www.schemastore.org/package"
            }
          ]
        }
      }
    }
  }
```
## DAP support
To debug deno programs, add this to .zed/debug.json
```
[
  {
    "adapter": "JavaScript",
    "label": "Deno",
    "request": "launch",
    "type": "pwa-node",
    "cwd": "$ZED_WORKTREE_ROOT",
    "program": "$ZED_FILE",
    "runtimeExecutable": "deno",
    "runtimeArgs": ["run", "--allow-all", "--inspect-wait"],
    "attachSimplePort": 9229
  }
]
```
## Runnable support
To run deno tasks like tests from the ui, add this to .zed/tasks.json
```
[
  {
    "label": "deno test",
    "command": "deno test -A '$ZED_FILE'",
    "tags": ["js-test"]
  }
]
```
## See also:
- TypeScript
- JavaScript