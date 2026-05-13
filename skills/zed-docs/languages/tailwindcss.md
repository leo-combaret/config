# Tailwind CSS
Zed has built-in support for Tailwind CSS autocomplete, linting, and hover previews.
- Language Server: tailwindlabs/tailwindcss-intellisense
Languages which can be used with Tailwind CSS in Zed:
- Astro
- CSS
- ERB
- Gleam
- HEEx
- HTML
- TypeScript
- JavaScript
- PHP
- Svelte
- Vue
## Configuration
If by default the language server isn't enough to make Tailwind work for a given language, you can configure the language server settings and add them to the lsp section of your settings.json :
```
{
  "lsp": {
    "tailwindcss-language-server": {
      "settings": {
        "classFunctions": ["cva", "cx"],
        "experimental": {
          "classRegex": ["[cls|className]\\s\\:\\=\\s\"([^\"]*)"]
        }
      }
    }
  }
}
```
Refer to the Tailwind CSS language server settings docs for more information.
### Using Tailwind CSS Mode in CSS Files
Zed includes support for the Tailwind CSS language mode, which provides full CSS IntelliSense support even when using Tailwind-specific at-rules like @apply , @layer , and @theme . Configure language servers in Settings ( cmd-,|ctrl-, ) under Languages > CSS, or add to your settings file:
```
{
  "languages": {
    "CSS": {
      "language_servers": [
        "tailwindcss-intellisense-css",
        "!vscode-css-language-server",
        "..."
      ]
    }
  }
}
```
The tailwindcss-intellisense-css language server serves as an alternative to the default CSS language server, maintaining all standard CSS IntelliSense features while adding support for Tailwind-specific syntax.
### Prettier Plugin
Zed supports Prettier out of the box, which means that if you have the Tailwind CSS Prettier plugin installed, adding it to your Prettier configuration will make it work automatically:
```
// .prettierrc
{
  "plugins": ["prettier-plugin-tailwindcss"]
}
```