# Helix Mode
Work in progress. Not all Helix keybindings are implemented yet.
Zed's Helix mode is an emulation layer that brings Helix-style keybindings and modal editing to Zed. It builds upon Zed's Vim mode , so much of the core functionality is shared. Enabling helix_mode will also enable vim_mode .
For a guide on Vim-related features that are also available in Helix mode, please refer to our Vim mode documentation .
To check the current status of Helix mode, or to request a missing Helix feature, see the "Are we Helix yet?" discussion .
For a detailed list of Helix's default keybindings, please visit the official Helix documentation .
## Core differences
Any text object that works with m i or m a also works with ] and [ , so for example ] ( selects the next pair of parentheses after the cursor.