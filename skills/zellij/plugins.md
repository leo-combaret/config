# Plugins
Zellij offers a Webassembly / WASI plugin system, allowing plugin developers to develop plugins in many different languages.
Zellij itself builds its UI from plugins, you can browse their code for inspiration.
## What is a Zellij Plugin?
A Zellij plugin is a first class citizen in the workspace, just like a terminal pane. It can render a UI , react to application state changes as well as control Zellij and change its behavior .
Our intention with the plugin system is to give users and developers the power to easily take full advantage of their terminal. Creating composable components that can be shared easily, turning everyday terminal tasks into a personalized multiplayer dashboard experience. We like to think of them as visual cross-platform scripts that do not need to be installed or compiled.
More importantly though, we feel that the best terminal workspace experience happens through collaboration. So - what do you think is a Zellij plugin?
Currently, Rust is the only language officially supported for plugins, but there are community efforts to support other languages as well.