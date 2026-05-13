# AI
Zed is an open-source AI code editor. AI runs throughout the editing experience: agents that read and write your code, inline transformations, code completions on every keystroke, and conversations with models in any buffer.
## How Zed approaches AI
Zed's AI features run inside a native, GPU-accelerated application built in Rust. There is no Electron layer between you and the model output.
- Open source. The editor and all AI features are open source . You can read how AI is implemented, how data flows to providers, and how tool calls execute.
- Multi-model. Use Zed's hosted models or bring your own API keys from Anthropic, OpenAI, Google, Ollama, and 8+ other providers. Run local models, connect to cloud APIs, or mix both. Switch models per task.
- External agents. Run Claude Agent, Gemini CLI, Codex, and other CLI-based agents directly in Zed through the Agent Client Protocol . See External Agents .
- Privacy by default. AI data sharing is opt-in. When you use your own API keys, Zed maintains zero-data retention agreements with providers. See Privacy and Security .
## Agentic editing
The Threads Sidebar is where you organize agent work. Start a thread, give it a task, and the agent reads, edits, and runs code in your project. You can run multiple threads at once, each using a different agent and working against different projects. See Tools for the capabilities available to Zed's built-in agent.
The Agent Panel is the conversation view for the active thread. Use it to send prompts, review changes, add context, and interact with the agent as it works.
You can extend agents with additional tools through MCP servers , control what they can access with tool permissions , and shape their behavior with rules .
The Inline Assistant works differently: select code or a terminal command, describe what you want, and the model rewrites the selection in place. It works with multiple cursors.
## Code completions
Edit Prediction provides AI code completions on every keystroke. Each keypress sends a request to the prediction provider, which returns single or multi-line suggestions you accept with tab .
The default provider is Zeta, Zed's open-source model trained on open data. You can also use GitHub Copilot, or Codestral.
## Getting started
- Configuration : Connect to Anthropic, OpenAI, Ollama, Google AI, or other LLM providers.
- Parallel Agents : Run multiple threads at once with the Threads Sidebar.
- External Agents : Run Claude Agent, Codex, Aider, or other external agents inside Zed.
- Subscription : Zed's hosted models and billing.
- Privacy and Security : How Zed handles data when using AI features.
New to Zed? Start with Getting Started , then come back here to set up AI. For a higher-level overview, see zed.dev/ai .