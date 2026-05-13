# How to Migrate from WebStorm to Zed
This guide covers how to set up Zed if you're coming from WebStorm, including keybindings, settings, and the differences you should expect as a JavaScript/TypeScript developer.
## Install Zed
Zed is available on macOS, Windows, and Linux.
For macOS, you can download it from zed.dev/download, or install via Homebrew:
```
brew install --cask zed
```
For Windows, download the installer from zed.dev/download, or install via winget:
```
winget install Zed.Zed
```
For most Linux users, the easiest way to install Zed is through our installation script:
```
curl -f https://zed.dev/install.sh | sh
```
After installation, you can launch Zed from your Applications folder (macOS), Start menu (Windows), or directly from the terminal using: zed . This opens the current directory in Zed.
## Set Up the JetBrains Keymap
If you're coming from WebStorm, the fastest way to feel at home is to use the JetBrains keymap. During onboarding, you can select it as your base keymap. If you missed that step, you can change it anytime:
1. Open Settings with cmd-,|ctrl-,
2. Search for Base Keymap
3. Select JetBrains
This maps familiar shortcuts like cmd-o|ctrl-alt-shift-n for Go to Class and shift shift|shift shift for Find Action.
## Set Up Editor Preferences
You can configure most settings in the Settings Editor ( cmd-,|ctrl-, ). For advanced settings, run zed: open settings file from the Command Palette to edit your settings file directly.
Settings WebStorm users typically configure first:
| Zed Setting | What it does |
| --- | --- |
| format_on_save | Auto-format when saving. Set to "on" to enable. |
| soft_wrap | Wrap long lines. Options: "none" , "editor_width" , "preferred_line_length" |
| preferred_line_length | Column width for wrapping and rulers. Default is 80. |
| inlay_hints | Show parameter names and type hints inline, like WebStorm's hints. |
| relative_line_numbers | Useful if you're coming from IdeaVim. |
Zed also supports per-project settings. Create a .zed/settings.json file in your project root to override global settings for that project, similar to how you might use .idea folders in WebStorm.
> Tip:
> If you're joining an existing project, check
> format_on_save
> before making your first commit. Otherwise you might accidentally reformat an entire file when you only meant to change one line.
## Open or Create a Project
After setup, use cmd-shift-n|ctrl-alt-n to open a folder. This becomes your workspace in Zed. Unlike WebStorm, there's no project configuration wizard, no framework selection dialog, and no project structure setup required.
To start a new project, create a directory using your terminal or file manager, then open it in Zed. The editor will treat that folder as the root of your project. For new projects, you'd typically run npm init , pnpm create , or your framework's CLI tool first, then open the resulting folder in Zed.
You can also launch Zed from the terminal inside any folder with: zed .
Once inside a project:
- Use cmd-shift-n|ctrl-alt-n to jump between files quickly (like WebStorm's "Recent Files")
- Use shift shift|shift shift to open the Command Palette (like WebStorm's "Search Everywhere")
- Use cmd-o|ctrl-alt-shift-n to search for symbols (like WebStorm's "Go to Symbol")
Open buffers appear as tabs across the top. The Project Panel shows your file tree and Git status. Toggle it with cmd-1|alt-1 (just like WebStorm's Project tool window).
## Differences in Keybindings
If you chose the JetBrains keymap during onboarding, most of your shortcuts should already feel familiar. Here's a quick reference of common actions and their keybindings with the JetBrains keymap active.
### Common Keybindings
| Action | Zed Keybinding |
| --- | --- |
| Command Palette | shift shift|shift shift |
| Go to File | cmd-shift-n|ctrl-alt-n |
| Go to Symbol | cmd-o|ctrl-alt-shift-n |
| File Outline | cmd-f12|ctrl-f12 |
| Go to Definition | cmd-b|ctrl-b |
| Find Usages | cmd-alt-f7|ctrl-alt-f7 |
| Rename Symbol | shift-f6|shift-f6 |
| Reformat Code | cmd-alt-l|ctrl-alt-l |
| Toggle Project Panel | cmd-1|alt-1 |
| Toggle Terminal | alt-f12|alt-f12 |
| Duplicate Line | cmd-d|ctrl-d |
| Delete Line | cmd-backspace|ctrl-y |
| Move Line Up | shift-alt-up|shift-alt-up |
| Move Line Down | shift-alt-down|shift-alt-down |
| Expand Selection | alt-up|ctrl-w |
| Shrink Selection | alt-down|ctrl-shift-w |
| Comment Line | cmd-/|ctrl-/ |
| Go Back | cmd-alt-left|ctrl-alt-left |
| Go Forward | cmd-alt-right|ctrl-alt-right |
| Toggle Breakpoint | ctrl-f8|ctrl-f8 |
| Navigate to Next Error | f2|f2 |
### Unique to Zed
| Action | Keybinding | Notes |
| --- | --- | --- |
| Toggle Right Dock | cmd-r|ctrl-alt-b | Agent panel, notifications |
| Split Pane Right | cmd-d|ctrl-shift-5 | Use other arrow keys to create splits in different directions |
### How to Customize Keybindings
- Open the Command Palette ( shift shift|shift shift )
- Run zed: open keymap
This opens a list of all available bindings. You can override individual shortcuts or remove conflicts.
Zed also supports key sequences (multi-key shortcuts).
## Differences in User Interfaces
### No Indexing
If you've used WebStorm on large projects, you know the wait. Opening a project with many dependencies can mean watching "Indexing..." for anywhere from 30 seconds to several minutes. WebStorm indexes your entire codebase and node_modules to power its code intelligence, and re-indexes when dependencies change.
Zed doesn't index. You open a folder and start coding immediately—no progress bars, no "Indexing paused" banners. File search and navigation stay fast regardless of project size or how many node_modules dependencies you have.
WebStorm's index enables features like finding all usages across your entire codebase, tracking import hierarchies, and flagging unused exports project-wide. Zed relies on language servers for this analysis, which may not cover as much ground.
How to adapt:
- Search symbols across the project with cmd-o|ctrl-alt-shift-n (powered by the TypeScript language server)
- Find files by name with cmd-shift-n|ctrl-alt-n
- Use cmd-shift-f|ctrl-shift-f for text search—it stays fast even in large monorepos
- Run tsc --noEmit or eslint . from the terminal when you need deeper project-wide analysis
### LSP vs. Native Language Intelligence
WebStorm has its own JavaScript and TypeScript analysis engine built by JetBrains. This engine understands your code deeply: it resolves types, tracks data flow, knows about framework-specific patterns, and offers specialized refactorings.
Zed uses the Language Server Protocol (LSP) for code intelligence. For JavaScript and TypeScript, Zed supports:
- vtsls (default) — Fast TypeScript language server with excellent performance
- typescript-language-server — The standard TypeScript LSP implementation
- ESLint — Linting integration
- Prettier — Code formatting (built-in)
The TypeScript LSP experience is well-supported. You get accurate completions, type checking, go-to-definition, and find-references. The experience is comparable to VS Code, which uses the same underlying TypeScript services.
Where you might notice differences:
- Framework-specific intelligence (Angular templates, Vue SFCs) may be less integrated
- Some complex refactorings (extract component with proper imports) may be less sophisticated
- Auto-import suggestions depend on what the language server knows about your project
How to adapt:
- Use alt-enter|alt-enter for available code actions—the list will vary by language server
- Ensure your tsconfig.json is properly configured so the language server understands your project structure
- Use Prettier for consistent formatting (it's enabled by default for JS/TS)
- For code inspection similar to WebStorm's "Inspect Code," check the Diagnostics panel ( cmd-6|alt-6 )—ESLint and TypeScript together catch many of the same issues
### No Project Model
WebStorm manages projects through .idea folders containing XML configuration files, framework detection, and run configurations. This model lets WebStorm remember your project settings, manage npm scripts through the UI, and persist run/debug setups.
Zed takes a different approach: a project is just a folder. There's no setup wizard, no framework detection dialog, no project structure to configure.
What this means in practice:
- Run configurations aren't a thing. Define reusable commands in tasks.json instead. Note that your existing .idea/ configurations won't carry over—you'll set up the ones you need fresh.
- npm scripts live in the terminal. Run npm run dev , pnpm build , or yarn test directly—there's no dedicated npm panel.
- No framework detection. Zed treats React, Angular, Vue, and vanilla JS/TS the same way.
How to adapt:
- Create a .zed/settings.json in your project root for project-specific settings
- Define common commands in tasks.json (open via Command Palette: zed: open tasks ):
```
[
  {
    "label": "dev",
    "command": "npm run dev"
  },
  {
    "label": "build",
    "command": "npm run build"
  },
  {
    "label": "test",
    "command": "npm test"
  },
  {
    "label": "test current file",
    "command": "npm test -- $ZED_FILE"
  }
]
```
- Use shift-f10|shift-f10 to run tasks quickly
- Lean on your terminal ( alt-f12|alt-f12 ) for anything tasks don't cover
### No Framework Integration
WebStorm's value for web development comes largely from its framework integration. React components get special treatment. Angular has dedicated tooling. Vue single-file components are fully understood. The npm tool window shows all your scripts.
Zed has none of this built-in. The TypeScript language server sees your code as TypeScript—it doesn't understand that a function is a React component or that a file is an Angular service.
How to adapt:
- Use grep and file search liberally. cmd-shift-f|ctrl-shift-f with a regex can find component definitions, route configurations, or API endpoints.
- Rely on your language server's "find references" ( cmd-alt-f7|ctrl-alt-f7 ) for navigation—it works, just without framework context
- Consider using framework-specific CLI tools ( ng , next , vite ) from Zed's terminal
- For React, JSX/TSX syntax and TypeScript types still provide good intelligence
> Tip:
> For projects with complex configurations, keep your framework's documentation handy. Zed's speed comes with less hand-holding for framework-specific features.
### Tool Windows vs. Docks
WebStorm organizes auxiliary views into numbered tool windows. Zed uses a similar concept called "docks":
| WebStorm Tool Window | Zed Equivalent | Zed Keybinding |
| --- | --- | --- |
| Project | Project Panel | cmd-1|alt-1 |
| Git | Git Panel | cmd-0|alt-0 |
| Terminal | Terminal Panel | alt-f12|alt-f12 |
| Structure | Outline Panel | cmd-7|alt-7 |
| Problems | Diagnostics | cmd-6|alt-6 |
| Debug | Debug Panel | cmd-5|alt-5 |
Zed has three dock positions: left, bottom, and right. Panels can be moved between docks by dragging or through settings.
Note that there's no dedicated npm tool window in Zed. Use the terminal or define tasks for your common npm scripts.
### Debugging
Both WebStorm and Zed offer integrated debugging for JavaScript and TypeScript:
- Zed uses vscode-js-debug (the same debug adapter that VS Code uses)
- Set breakpoints with ctrl-f8|ctrl-f8
- Start debugging with alt-shift-f9|alt-shift-f9
- Step through code with f7|f7 (step into), f8|f8 (step over), shift-f8|shift-f8 (step out)
- Continue execution with f9|f9
Zed can debug:
- Node.js applications and scripts
- Chrome/browser JavaScript
- Jest, Mocha, Vitest, and other test frameworks
- Next.js (both server and client-side)
For more control, create a .zed/debug.json file:
```
[
  {
    "label": "Debug Current File",
    "adapter": "JavaScript",
    "program": "$ZED_FILE",
    "request": "launch"
  },
  {
    "label": "Debug Node Server",
    "adapter": "JavaScript",
    "request": "launch",
    "program": "${workspaceFolder}/src/server.js"
  },
  {
    "label": "Attach to Chrome",
    "adapter": "JavaScript",
    "request": "attach",
    "port": 9222
  }
]
```
Zed also recognizes .vscode/launch.json configurations, so existing VS Code debug setups often work out of the box.
### Running Tests
WebStorm has a dedicated test runner with a visual interface showing pass/fail status for each test. Zed provides test running through:
- Gutter icons — Click the play button next to test functions or describe blocks
- Tasks — Define test commands in tasks.json
- Terminal — Run npm test , jest , vitest , etc. directly
Zed supports auto-detection for common test frameworks:
- Jest
- Mocha
- Vitest
- Jasmine
- Bun test
- Node.js test runner
The test output appears in the terminal panel. For Jest, use --verbose for detailed output or --watch for continuous testing during development.
### Extensions vs. Plugins
WebStorm has a plugin catalog covering additional language support, themes, and tool integrations.
Zed's extension catalog is smaller and more focused:
- Language support and syntax highlighting
- Themes
- Context servers
Several features that require plugins in WebStorm are built into Zed:
- Real-time collaboration with voice chat
- AI coding assistance
- Built-in terminal
- Task runner
- LSP-based code intelligence
- Prettier formatting
- ESLint integration
### What's Not in Zed
To set expectations clearly, here's what WebStorm offers that Zed doesn't have:
- npm tool window — Use the terminal or tasks instead
- HTTP Client — Use tools like Postman, Insomnia, or curl
- Database tools — Use DataGrip, DBeaver, or TablePlus
- Framework-specific tooling (Angular schematics, React refactorings) — Use CLI tools
- Visual package.json editor — Edit the file directly
- Built-in REST client — Use external tools or extensions
- Profiler integration — Use Chrome DevTools or Node.js profiling tools
## Collaboration in Zed vs. WebStorm
WebStorm offers Code With Me as a separate feature for collaboration. Zed has collaboration built into the core experience.
- Open the Collab Panel in the left dock
- Create a channel and invite your collaborators to join
- Share your screen or your codebase directly
Once connected, you'll see each other's cursors, selections, and edits in real time. Voice chat is included. There's no need for separate tools or third-party logins.
## Using AI in Zed
If you're used to AI assistants in WebStorm (like GitHub Copilot, JetBrains AI Assistant, or Junie), Zed offers similar capabilities with more flexibility.
### Configuring GitHub Copilot
1. Open Settings with cmd-,|ctrl-,
2. Navigate to AI → Edit Predictions
3. Click Configure next to "Configure Providers"
4. Under GitHub Copilot , click Sign in to GitHub
Once signed in, just start typing. Zed will offer suggestions inline for you to accept.
### Additional AI Options
To use other AI models in Zed, you have several options:
- Use Zed's hosted models, with higher rate limits. Requires authentication and subscription to Zed Pro .
- Bring your own API keys , no authentication needed
- Use external agents like Claude Agent
## Advanced Config and Productivity Tweaks
Zed exposes advanced settings for power users who want to fine-tune their environment.
Here are a few useful tweaks for JavaScript/TypeScript developers:
Format on Save:
```
"format_on_save": "on"
```
Configure Prettier as the default formatter (requires manual JSON editing):
```
{
  "formatter": {
    "external": {
      "command": "prettier",
      "arguments": ["--stdin-filepath", "{buffer_path}"]
    }
  }
}
```
Enable ESLint code actions (requires manual JSON editing):
```
{
  "lsp": {
    "eslint": {
      "settings": {
        "codeActionOnSave": {
          "rules": ["import/order"]
        }
      }
    }
  }
}
```
Configure TypeScript strict mode hints:
In your tsconfig.json , enable strict mode for better type checking:
```
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```
Enable direnv support (useful for projects using direnv for environment variables):
```
"load_direnv": "shell_hook"
```
## Next Steps
Now that you're set up, here are some resources to help you get the most out of Zed:
- All Settings — Customize settings, themes, and editor behavior
- Key Bindings — Learn how to customize and extend your keymap
- Tasks — Set up build and run commands for your projects
- AI Features — Explore Zed's AI capabilities beyond code completion
- Collaboration — Share your projects and code together in real time
- JavaScript in Zed — JavaScript-specific setup and configuration
- TypeScript in Zed — TypeScript-specific setup and configuration