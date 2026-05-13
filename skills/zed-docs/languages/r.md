# R
R support is available via multiple R Zed extensions:
- ocsmit/zed-r Tree-sitter: r-lib/tree-sitter-r Language-Server: REditorSupport/languageserver
- posit-dev/air Formatter: posit-dev/air
## Installation
1. Download and Install R .
2. Install the R packages languageserver and lintr :
```
install.packages("languageserver")
install.packages("lintr")
```
1. Install the R extension through Zed's extensions manager for basic R language support (syntax highlighting, tree-sitter support) and for REditorSupport/languageserver support.
2. Install the Air extension through Zed's extensions manager for R code formatting via Air.
## Linting
REditorSupport/languageserver bundles support for r-lib/lintr as a linter. This can be configured via the use of a .lintr inside your project (or in your home directory for global defaults).
```
linters: linters_with_defaults(
    line_length_linter(120),
    commented_code_linter = NULL
  )
exclusions: list(
    "inst/doc/creating_linters.R" = 1,
    "inst/example/bad.R",
    "tests/testthat/exclusions-test"
  )
```
Or exclude it from linting anything,
```
exclusions: list(".")
```
See Using lintr for a complete list of options,
## Formatting
### Air
Air provides code formatting for R, including support for format-on-save. The Air documentation for Zed contains the most up-to-date advice for running Air in Zed.
Ensure that you have installed both the ocsmit/zed-r extension (for general R language awareness in Zed) and the Air extension.
Configure language servers in Settings ( cmd-,|ctrl-, ) under Languages > R, or add to your settings file:
```
{
  "languages": {
    "R": {
      "language_servers": ["air"]
    }
  }
}
```
If you use the "r_language_server" from REditorSupport/languageserver , but would still like to use Air for formatting, configure in Settings ( cmd-,|ctrl-, ) under Languages > R, or add to your settings file:
```
{
  "languages": {
    "R": {
      "language_servers": ["air", "r_language_server"],
      "use_on_type_format": false
    }
  }
}
```
Note that "air" must come first in this list, otherwise r-lib/styler will be invoked via "r_language_server" .
"r_language_server" provides on-type-formatting that differs from Air's formatting rules. To avoid this entirely and let Air be fully in charge of formatting your R files, also set "use_on_type_format": false as shown above.
#### Configuring Air
Air is minimally configurable via an air.toml file placed in the root folder of your project:
```
[format]
line-width = 80
indent-width = 2
```
For more details, refer to the Air documentation about configuration .
### Styler
REditorSupport/languageserver bundles support for r-lib/styler as a formatter. See Customizing Styler for more information on how to customize its behavior.