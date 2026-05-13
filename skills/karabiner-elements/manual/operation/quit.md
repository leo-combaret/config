# Quit
Karabiner-Elements keeps running in the background even if you close the settings window. To quit Karabiner-Elements, choose “Quit Karabiner-Elements” from menu bar.
If you’ve hidden the menu bar icon, you can also quit Karabiner-Elements from Settings.
If you want to terminate Karabiner-Elements from the command line, execute the following commands:
```
'/Library/Application Support/org.pqrs/Karabiner-Elements/Karabiner-Elements Non-Privileged Agents v2.app/Contents/MacOS/Karabiner-Elements Non-Privileged Agents v2'
 unregister-core-agents

'/Library/Application Support/org.pqrs/Karabiner-Elements/Karabiner-Elements Non-Privileged Agents v2.app/Contents/MacOS/Karabiner-Elements Non-Privileged Agents v2'
 unregister-menu-agent

'/Library/Application Support/org.pqrs/Karabiner-Elements/Karabiner-Elements Non-Privileged Agents v2.app/Contents/MacOS/Karabiner-Elements Non-Privileged Agents v2'
 unregister-multitouch-extension-agent

'/Library/Application Support/org.pqrs/Karabiner-Elements/Karabiner-Elements Non-Privileged Agents v2.app/Contents/MacOS/Karabiner-Elements Non-Privileged Agents v2'
 unregister-notification-window-agent
```