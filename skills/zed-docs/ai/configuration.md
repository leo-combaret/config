# Configuration
You can configure multiple dimensions of AI usage in Zed:
1. Which LLM providers you can use Zed's hosted models, which require authentication and subscription Using your own API keys , which do not require the above Using external agents like Claude Agent , which also do not require the above
2. Model parameters and usage
3. Interactions with the Agent Panel
## Turning AI Off Entirely
To disable all AI features, add the following to your settings file ( how to edit ):
```
{
  "disable_ai": true
}
```
See this blog post for further context on this option.