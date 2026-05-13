# Restart
You can restart Karabiner-Elements from the menu bar or Settings.
If you want to restart Karabiner-Elements from the command line, execute the following command:
```
launchctl kickstart -k gui/
$(
id -u
)
/org.pqrs.service.agent.karabiner_console_user_server
```