# Astro
Astro support is available through the Astro extension .
- Tree-sitter: virchau13/tree-sitter-astro
- Language Server: withastro/language-tools
## Using the Tailwind CSS Language Server with Astro
To get all the features (autocomplete, linting, etc.) from the Tailwind CSS language server in Astro files, you need to configure the language server so that it knows about where to look for CSS classes by adding the following to your settings.json :
```
{
  "lsp": {
    "tailwindcss-language-server": {
      "settings": {
        "includeLanguages": {
          "astro": "html"
        },
        "experimental": {
          "classRegex": [
            "class=\"([^\"]*)\"",
            "class='([^']*)'",
            "class:list=\"{([^}]*)}\"",
            "class:list='{([^}]*)}'"
          ]
        }
      }
    }
  }
}
```
With these settings, you will get completions for Tailwind CSS classes in Astro template files. Examples:
```
---
const active = true;
---

<!-- Standard class attribute -->
<div class="flex items-center <completion here>">
  <p class="text-lg font-bold <completion here>">Hello World</p>
</div>

<!-- class:list directive -->
<div class:list={["flex", "items-center", "<completion here>"]}>
  Content
</div>

<!-- Conditional classes -->
<div class:list={{ "flex <completion here>": active, "hidden <completion here>": !active }}>
  Content
</div>
```