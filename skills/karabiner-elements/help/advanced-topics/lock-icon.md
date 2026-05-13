# What is the lock indicator on Karabiner-Elements and Karabiner-EventViewer icon
This content is for older versions of Karabiner Elements.
Prior to Karabiner-Elements 14.10.0, a lock indicator is shown on Karabiner-Elements and Karabiner-EventViewer icon.
These indicators show that these files are protected so that they cannot be deleted from Finder.
## Why these files are protected
This protection is intended to prevent incomplete uninstallation.
Karabiner-Elements is a system-wide software, and files are installed in appropriate locations besides the Applications folder.
Therefore, if you just put the application icon in Trash like a normal app uninstallation, some files will be left behind.
The file protection forces to use the built-in uninstaller and remove installed files properly at the uninstallation.
This file locking is achieved with schg and uchg flags.
You can unlock these files by running the following commands in Terminal. (Administrator password is required to run the commands.)
```
sudo chflags nouchg,noschg /Applications/Karabiner-Elements.app

sudo chflags nouchg,noschg /Applications/Karabiner-EventViewer.app
```
In particular, if Full Disk Access rights have not been granted to Terminal, “Operation not permitted” error may be displayed. In this case, the safest solution is to grant App Management rights to Terminal.