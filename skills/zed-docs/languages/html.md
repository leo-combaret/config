# HTML
HTML support is available through the HTML extension .
- Tree-sitter: tree-sitter/tree-sitter-html
- Language Server: microsoft/vscode-html-languageservice
This extension is automatically installed, but if you do not want to use it, you can add the following to your settings:
```
{
  "auto_install_extensions": {
    "html": false
  }
}
```
## Formatting
By default Zed uses Prettier for formatting HTML.
Configure formatting in Settings ( cmd-,|ctrl-, ) under Languages > HTML, or add to your settings file:
```
"languages": {
    "HTML": {
      "format_on_save": "off",
    }
  }
```
You can still trigger formatting manually with cmd-shift-i|ctrl-shift-i or by opening the command palette ( cmd-shift-p|ctrl-shift-p ) and selecting "Format Document".
### LSP Formatting
To use the vscode-html-language-server language server auto-formatting instead of Prettier, configure the formatter in Settings ( cmd-,|ctrl-, ) under Languages > HTML, or add to your settings file:
```
"languages": {
    "HTML": {
      "formatter": "language_server",
    }
  }
```
You can customize various formatting options for vscode-html-language-server via your Zed settings.json :
```
"lsp": {
    "vscode-html-language-server": {
      "settings": {
        "html": {
          "format": {
            // Indent under <html> and <head> (default: false)
            "indentInnerHtml": true,
            // Disable formatting inside <svg> or <script>
            "contentUnformatted": "svg,script",
            // Add an extra newline before <div> and <p>
            "extraLiners": "div,p"
          }
        }
      }
    }
  }
```
## Using the Tailwind CSS Language Server with HTML
To get all the features (autocomplete, linting, etc.) from the Tailwind CSS language server in HTML files, you need to configure the language server so that it knows about where to look for CSS classes by adding the following to your settings.json :
```
{
  "lsp": {
    "tailwindcss-language-server": {
      "settings": {
        "experimental": {
          "classRegex": ["class=\"([^\"]*)\""]
        }
      }
    }
  }
}
```
With these settings, you will get completions for Tailwind CSS classes in HTML class attributes. Examples:
```
<div class="flex items-center <completion here>">
  <p class="text-lg font-bold <completion here>">Hello World</p>
</div>
```
## See also
- CSS
- JavaScript
- TypeScript