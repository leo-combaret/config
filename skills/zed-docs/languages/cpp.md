# C++
C++ support is available natively in Zed.
- Tree-sitter: tree-sitter/tree-sitter-cpp
- Language Server: clangd/clangd
## Binary
You can configure which clangd binary Zed should use.
By default, Zed will try to find a clangd in your $PATH and try to use that. If that binary successfully executes, it's used. Otherwise, Zed will fall back to installing its own clangd version and use that.
If you want to install a pre-release clangd version instead you can instruct Zed to do so by setting pre_release to true in your settings.json :
```
{
  "lsp": {
    "clangd": {
      "fetch": {
        "pre_release": true
      }
    }
  }
}
```
If you want to disable Zed looking for a clangd binary, you can set ignore_system_version to true in your settings.json :
```
{
  "lsp": {
    "clangd": {
      "binary": {
        "ignore_system_version": true
      }
    }
  }
}
```
If you want to use a binary in a custom location, you can specify a path and optional arguments :
```
{
  "lsp": {
    "clangd": {
      "binary": {
        "path": "/path/to/clangd",
        "arguments": []
      }
    }
  }
}
```
This "path" has to be an absolute path.
## Arguments
You can pass any number of arguments to clangd. To see a full set of available options, run clangd --help from the command line. For example with --function-arg-placeholders=0 completions contain only parentheses for function calls, while the default ( --function-arg-placeholders=1 ) completions also contain placeholders for method parameters.
```
{
  "lsp": {
    "clangd": {
      "binary": {
        "path": "/path/to/clangd",
        "arguments": ["--function-arg-placeholders=0"]
      }
    }
  }
}
```
## Formatting
By default Zed will use the clangd language server for formatting C++ code. The Clangd is the same as the clang-format CLI tool. To configure this you can add a .clang-format file. For example:
```
# yaml-language-server: $schema=https://json.schemastore.org/clang-format-21.x.json
---
BasedOnStyle: LLVM
IndentWidth: 4
---
Language: Cpp
# Force pointers to the type for C++.
DerivePointerAlignment: false
PointerAlignment: Left
---
```
See Clang-Format Style Options for a complete list of options.
You can trigger formatting via cmd-shift-i|ctrl-shift-i or the editor: format action from the command palette or by enabling format on save.
Configure formatting in Settings ( cmd-,|ctrl-, ) under Languages > C++, or add to your settings file:
```
"languages": {
    "C++": {
      "format_on_save": "on",
      "tab_size": 2
    }
  }
```
## More server configuration
In the root of your project, it is generally common to create a .clangd file to set extra configuration.
```
# yaml-language-server: $schema=https://json.schemastore.org/clangd.json
CompileFlags:
  Add:
    - "--include-directory=/path/to/include"
Diagnostics:
  MissingIncludes: Strict
  UnusedIncludes: Strict
```
For more advanced usage of clangd configuration file, take a look into their official page .
## Compile Commands
For some projects Clangd requires a compile_commands.json file to properly analyze your project. This file contains the compilation database that tells clangd how your project should be built.
### CMake Compile Commands
With CMake, you can generate compile_commands.json automatically by adding the following line to your CMakeLists.txt :
```
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```
After building your project, CMake will generate the compile_commands.json file in the build directory and clangd will automatically pick it up.
## Debugging
You can use CodeLLDB or GDB to debug native binaries. (Make sure that your build process passes -g to the C++ compiler, so that debug information is included in the resulting binary.) See below for examples of debug configurations that you can add to .zed/debug.json .
- CodeLLDB configuration documentation
- GDB configuration documentation GDB needs to be at least v14.1
### Build and Debug Binary
```
[
  {
    "label": "Debug native binary",
    "build": {
      "command": "make",
      "args": ["-j8"],
      "cwd": "$ZED_WORKTREE_ROOT"
    },
    "program": "$ZED_WORKTREE_ROOT/build/prog",
    "request": "launch",
    "adapter": "CodeLLDB"
  }
]
```
## Protocol Extensions
Zed currently implements the following clangd extensions :
### Inactive Regions
Automatically dims inactive sections of code due to preprocessor directives, such as #if , #ifdef , or #ifndef blocks that evaluate to false.
### Switch Between Source and Header Files
Allows switching between corresponding C++ source files (e.g., .cpp ) and header files (e.g., .h ). by running the command editor: switch source header from the command palette or by setting a keybinding for the editor::SwitchSourceHeader action.
```
{
  "context": "Editor",
  "bindings": {
    "alt-enter": "editor::SwitchSourceHeader"
  }
}
```