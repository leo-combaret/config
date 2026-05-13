# Set environment variables
Karabiner-Elements references several environment variables internally. Additionally, the shell_command and open_application used in Complex Modifications are also affected by environment variables. To support this, we provide a way to define them.
Karabiner-Elements loads environment variables from /Library/Application Support/org.pqrs/config/karabiner_environment if the file exists. If you define PATH and others there, shell commands and opened apps via shell_command and open_application inherit these environment variables.
## Example
You need to run your editor with root privileges to edit the karabiner_environment file. For example, you can edit it by running the following commands in Terminal.
```
sudo nano 
'/Library/Application Support/org.pqrs/config/karabiner_environment'
```
Here is an example of the karabiner_environment file.
```
# Add ~/opt/bin to PATH

PATH
=
$HOME
/opt/bin:
$PATH

# Set locale

LC_ALL
=
C
```
- Define environment variables one per line.
- Any text following # is treated as a comment.
- Existing environment variables (e.g., $HOME) are expanded.
After modifying the karabiner_environment file, you need to restart the karabiner_console_user_server process to apply the changes. You can do it by running the following commands in Terminal.
```
launchctl kickstart -k gui/
$(
id -u
)
/org.pqrs.service.agent.karabiner_console_user_server
```
Do not put sensitive information (e.g., API keys) in karabiner_environment . If multiple people use your Mac, all users on the machine can read this file, so only include information that is safe to share.
Additionally, the environment variables defined in karabiner_environment are also logged as shown below.
```
[info] [console_user_server] setenv: PATH = /Users/tekezo/opt/bin:/usr/bin:/bin:/usr/sbin:/sbin

[info] [console_user_server] setenv: LC_ALL = C
```
## Change where karabiner.json is saved
You can also use this mechanism to change where Karabiner-Elements stores its files. The two environment variables used for this are:
- XDG_CONFIG_HOME
- XDG_DATA_HOME
For example, the following configuration changes the karabiner.json location under ~/Library/Application Support.
```
XDG_CONFIG_HOME
=
$HOME
/Library/Application Support/org.pqrs/config

XDG_DATA_HOME
=
$HOME
/Library/Application Support/org.pqrs/data
```
Note: karabiner.json is stored at $XDG_CONFIG_HOME/karabiner/karabiner.json .
After changing XDG_CONFIG_HOME or XDG_DATA_HOME, you need to restart the Karabiner-Elements user processes. The most reliable way is to sign out and back in, or reboot macOS.
Unless you have a strong reason, we do not recommend changing file locations via XDG_CONFIG_HOME.
You can relocate files by using a symbolic link instead, so we recommend using a symbolic link.