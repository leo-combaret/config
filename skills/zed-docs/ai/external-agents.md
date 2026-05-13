# External Agents
Zed supports many external agents, including CLI-based ones, through the Agent Client Protocol (ACP) .
Zed supports Gemini CLI (the reference ACP implementation), Claude Agent , Codex , GitHub Copilot , and additional agents you can configure.
For Zed's built-in agent and the full list of tools it can use natively, see Agent Tools .
> Note that Zed's interaction with external agents is strictly UI-based; the billing, legal, and terms arrangement is directly between you and the agent provider.
> Zed does not charge for use of external agents, and our
> zero-data retention agreements/privacy guarantees
> are
> only
> applicable for Zed's hosted models.
## Gemini CLI
Zed provides the ability to run Gemini CLI directly in the agent panel . Under the hood we run Gemini CLI in the background, and talk to it over ACP.
### Getting Started
First open the agent panel with cmd-?|ctrl-? , and then use the + button in the top right to start a new Gemini CLI thread.
If you'd like to bind this to a keyboard shortcut, you can do so by editing your keymap.json file via the zed: open keymap file command to include:
```
[
  {
    "bindings": {
      "cmd-alt-g": [
        "agent::NewExternalAgentThread",
        { "agent": { "custom": { "name": "gemini" } } }
      ]
    }
  }
]
```
#### Installation
The first time you create a Gemini CLI thread, Zed will install @google/gemini-cli . This installation is only available to Zed and is kept up to date as you use the agent.
#### Authentication
After you have Gemini CLI running, you'll be prompted to authenticate.
Click the "Login" button to open the Gemini CLI interactively, where you can log in with your Google account or Vertex AI credentials. Zed does not see your OAuth or access tokens in this case.
If the GEMINI_API_KEY environment variable (or GOOGLE_AI_API_KEY ) is already set, or you have configured a Google AI API key in Zed's language model provider settings , it will be passed to Gemini CLI automatically.
For more information, see the Gemini CLI docs .
### Usage
Gemini CLI supports the same workflows as Zed's first-party agent: code generation, refactoring, debugging, and Q&A. Add context by @-mentioning files, recent threads, or symbols.
> Some agent panel features are not yet available with Gemini CLI: editing past messages, resuming threads from history, and checkpointing.
## Claude Agent
Similar to Gemini CLI, you can also run Claude Agent directly via Zed's agent panel . Under the hood, Zed runs the Claude Agent SDK, which runs Claude Code under the hood, and communicates to it over ACP, through a dedicated adapter .
### Getting Started
Open the agent panel with cmd-?|ctrl-? , and then use the + button in the top right to start a new Claude Agent thread.
If you'd like to bind this to a keyboard shortcut, you can do so by editing your keymap.json file via the zed: open keymap file command to include:
```
[
  {
    "bindings": {
      "cmd-alt-c": [
        "agent::NewExternalAgentThread",
        { "agent": { "custom": { "name": "claude-acp" } } }
      ]
    }
  }
]
```
### Authentication
As of version 0.202.7 , authentication to Zed's Claude Agent installation is decoupled entirely from Zed's agent. That is to say, an Anthropic API key added via the Zed Agent's settings will not be utilized by Claude Agent for authentication and billing.
To ensure you're using your billing method of choice, open a new Claude Agent thread . Then, run /login , and authenticate either via API key, or via Log in with Claude Code to use a Claude Pro/Max subscription.
#### Installation
The first time you create a Claude Agent thread, Zed will install @zed-industries/claude-agent-acp . This installation is only available to Zed and is kept up to date as you use the agent.
Zed will always use this managed version of the Claude Agent adapter, which includes a vendored version of the Claude Code CLI, even if you have it installed globally.
If you want to override the executable used by the adapter, you can set the CLAUDE_CODE_EXECUTABLE environment variable in your settings to the path of your preferred executable.
```
{
  "agent_servers": {
    "claude-acp": {
      "type": "registry",
      "env": {
        "CLAUDE_CODE_EXECUTABLE": "/path/to/alternate-claude-code-executable"
      }
    }
  }
}
```
### Usage
Claude Agent supports the same workflows as Zed's first-party agent. Add context by @-mentioning files, recent threads, diagnostics, or symbols.
In complement to talking to it over ACP , Zed relies on the Claude Agent SDK to support some of its specific features. However, the SDK doesn't yet expose everything needed to fully support all of them:
- Slash Commands: Custom slash commands are fully supported, and have been merged into skills. A subset of built-in commands are supported.
- Subagents are supported.
- Agent teams are currently not supported.
- Hooks are currently not supported.
> Some
> agent panel
> features are not yet available with Claude Agent: editing past messages, resuming threads from history, and checkpointing.
#### CLAUDE.md
Claude Agent in Zed will automatically use any CLAUDE.md file found in your project root, project subdirectories, or root .claude directory.
If you don't have a CLAUDE.md file, you can ask Claude Agent to create one for you through the init slash command.
## Codex CLI
You can also run Codex CLI directly via Zed's agent panel . Under the hood, Zed runs Codex CLI and communicates to it over ACP, through a dedicated adapter .
### Getting Started
As of version 0.208 , you should be able to use Codex directly from Zed. Open the agent panel with cmd-?|ctrl-? , and then use the + button in the top right to start a new Codex thread.
If you'd like to bind this to a keyboard shortcut, you can do so by editing your keymap.json file via the zed: open keymap file command to include:
```
[
  {
    "bindings": {
      "cmd-alt-c": [
        "agent::NewExternalAgentThread",
        { "agent": { "custom": { "name": "codex-acp" } } }
      ]
    }
  }
]
```
### Authentication
Authentication to Zed's Codex installation is decoupled entirely from Zed's agent. That is to say, an OpenAI API key added via the Zed Agent's settings will not be utilized by Codex for authentication and billing.
To ensure you're using your billing method of choice, open a new Codex thread . The first time you will be prompted to authenticate with one of three methods:
1. Login with ChatGPT - allows you to use your existing, paid ChatGPT subscription. Note: This method isn't currently supported in remote projects
2. CODEX_API_KEY - uses an API key you have set in your environment under the variable CODEX_API_KEY .
3. OPENAI_API_KEY - uses an API key you have set in your environment under the variable OPENAI_API_KEY .
If you are already logged in and want to change your authentication method, type /logout in the thread and authenticate again.
If you want to use a third-party provider with Codex, you can configure that with your Codex config.toml or pass extra args/env variables to your Codex agent servers settings.
#### Installation
The first time you create a Codex thread, Zed will install codex-acp . This installation is only available to Zed and is kept up to date as you use the agent.
Zed will always use this managed version of Codex even if you have it installed globally.
### Usage
Codex supports the same workflows as Zed's first-party agent. Add context by @-mentioning files or symbols.
> Some agent panel features are not yet available with Codex: editing past messages, resuming threads from history, and checkpointing.
## Add More Agents
### Via Agent Server Extensions
Starting from v0.221.x , the ACP Registry is the preferred way to install external agents in Zed. Learn more about it in the release blog post . At some point in the near future, Agent Server extensions will be deprecated.
Add more external agents to Zed by installing Agent Server extensions .
See what agents are available by filtering for "Agent Servers" in the extensions page, which you can access via the command palette with zed: extensions , or the Zed website .
### Via The ACP Registry
#### Overview
As mentioned above, the Agent Server extensions will be deprecated in the near future to give room to the ACP Registry.
The ACP Registry lets developers distribute ACP-compatible agents to any client that implements the protocol. Agents installed from the registry update automatically.
At the moment, the registry is a curated set of agents, including only the ones that support authentication .
#### Using it in Zed
Use the zed: acp registry command to quickly go to the ACP Registry page. There's also a button ("Add Agent") that takes you there in the agent panel's configuration view.
From there, you can click to install your preferred agent and it will become available right away in the + icon button in the agent panel.
> If you installed the same agent through both the extension and the registry, the registry version takes precedence.
### Custom Agents
You can also add agents through your settings file ( how to edit ) by specifying certain fields under agent_servers , like so:
```
{
  "agent_servers": {
    "My Custom Agent": {
      "type": "custom",
      "command": "node",
      "args": ["~/projects/agent/index.js", "--acp"],
      "env": {}
    }
  }
}
```
This can be useful if you're in the middle of developing a new agent that speaks the protocol and you want to debug it.
It's also possible to customize environment variables for registry-installed agents like Claude Agent, Codex, and Gemini CLI by using their registry names ( claude-acp , codex-acp , gemini ) with "type": "registry" in your settings.
## Debugging Agents
When using external agents in Zed, you can access the debug view via with dev: open acp logs from the Command Palette. This lets you see the messages being sent and received between Zed and the agent.
It's helpful to attach data from this view if you're opening issues about problems with external agents like Claude Agent, Codex, OpenCode, etc.
## Configuration Boundaries
External agents run as separate processes that communicate with Zed via the Agent Client Protocol (ACP) . This creates important boundaries between Zed's configuration and the agent's native configuration.
### What Zed Forwards to External Agents
When you start an external agent thread, Zed sends:
| Setting | How to Configure |
| --- | --- |
| Model selection | agent_servers.<agent>.default_model in settings |
| Mode selection | agent_servers.<agent>.default_mode in settings |
| Environment variables | agent_servers.<agent>.env in settings |
| MCP servers | context_servers in settings (see limitations ) |
| Working directory | Automatically set to project root |
Not forwarded:
- Profiles — profiles only apply to Zed's first-party agent
- Tool permissions settings — external agents request permissions at runtime via UI prompts
- Rules files — Zed's rules system only applies to Zed's first-party agent (external agents read their own rules files directly)
### What External Agents Read Directly
External agents run as CLI tools with full filesystem access. They read their own configuration files directly — Zed doesn't forward or block these.
#### Claude Agent
Claude Agent runs Claude Code under the hood, which reads its standard configuration:
| Config | Read by Claude Agent? |
| --- | --- |
| ~/.claude/ directory | Yes — Claude Code reads its own settings and memory |
| CLAUDE.md files | Yes — Claude Code reads these directly from the project |
| Skills | Yes — exposed via the Claude Agent SDK |
| MCP servers from Claude Code config | Yes — but Zed also forwards its own MCP servers via ACP |
| Hooks | No — not supported |
| Authentication | Separate — you must authenticate via /login in Zed |
> Why separate authentication?
> Zed isolates Claude Agent authentication to give you control over which account and billing method you use.
#### Codex
Codex runs the Codex CLI under the hood, which reads its standard configuration:
| Config | Read by Codex? |
| --- | --- |
| ~/.codex/config.toml | Yes — Codex CLI reads its own config |
| MCP servers from Codex config | Yes — but Zed also forwards its own MCP servers |
| CODEX_API_KEY env var | Yes — inherited from your shell environment |
| OPENAI_API_KEY env var | Yes — inherited from your shell environment |
| ChatGPT OAuth login | Separate — you must re-authenticate in Zed |
You can also pass environment variables through Zed settings:
```
{
  "agent_servers": {
    "codex-acp": {
      "type": "registry",
      "env": {
        "CODEX_API_KEY": "your-key",
        "CUSTOM_PROVIDER_URL": "https://..."
      }
    }
  }
}
```
### MCP Server Access
MCP servers configured in Zed's context_servers are forwarded to Claude Agent and Codex via the ACP protocol.
- Local stdio-based MCP servers: Work reliably
- Remote MCP servers with OAuth: May have issues ( #54410 )
External agents can access MCP servers from two sources: Zed's context_servers (forwarded via ACP) and their own native configuration files ( ~/.claude/ , ~/.codex/config.toml ).
For more on configuring MCP servers, see Model Context Protocol .
### Troubleshooting
"I enabled MCP tools in Zed but the agent can't see them"
1. Verify the MCP server is enabled in context_servers settings
2. For remote MCP servers with OAuth, this is a known issue — try local stdio-based servers instead
3. Open dev: open acp logs from the Command Palette to debug
"My existing Claude Code / Codex setup isn't working in Zed"
External agents read their own config files, but authentication is handled separately:
1. Re-authenticate via /login (Claude Agent) or the authentication prompt (Codex)
2. Your existing MCP servers and settings from ~/.claude/ or ~/.codex/config.toml should work
3. You can also configure additional settings via agent_servers.<agent>.env in Zed
"Profiles don't affect my external agent"
Correct — profiles only apply to Zed's first-party agent. External agents have their own tool sets and don't use Zed's profile system.