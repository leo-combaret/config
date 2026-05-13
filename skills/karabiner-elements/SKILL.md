---
name: karabiner-elements
description: "Documentation for karabiner-elements.pqrs.org. Use when the user asks about Karabiner-Elements for macOS, karabiner.json, complex_modifications, Simple Modifications, Function Keys, Karabiner-EventViewer, karabiner_cli, device/profile configuration, virtual HID permissions, or troubleshooting keyboard remapping from https://karabiner-elements.pqrs.org/docs. Trigger on mentions of 'Karabiner-Elements', 'karabiner.json', 'complex_modifications', 'Karabiner-EventViewer', 'karabiner_cli', 'pqrs.org', or macOS keyboard customization."
---

# Karabiner-Elements Documentation

> 124 pages from [https://karabiner-elements.pqrs.org/docs](https://karabiner-elements.pqrs.org/docs)

## Overview

Karabiner-Elements is a macOS keyboard customizer for remapping keys, function keys, pointing buttons, and device-specific behavior. These docs cover installation and required macOS permissions, the Settings UI workflow, EventViewer, profiles, device settings, command-line operations, and security architecture. The largest section is the Karabiner Configuration Reference Manual, which documents `karabiner.json`, `complex_modifications`, manipulator `from` and `to` definitions, conditions, variables, software functions, mouse handling, and examples.

## Contents

### Getting Started

- [Documentation](index.md)
- [Getting started](getting-started.md)
  - [Installation](getting-started/installation.md)
  - [Features](getting-started/features.md)

### Manual

- [Manual](manual.md)
- [Configuration](manual/configuration.md)
  - [Change a key to another key](manual/configuration/configure-simple-modifications.md)
  - [Use more complex modifications](manual/configuration/configure-complex-modifications.md)
  - [Add your own complex modifications](manual/configuration/add-your-own-complex-modifications.md)
  - [Edit complex modifications](manual/configuration/edit-complex-modifications.md)
  - [Add your own complex modifications (using JavaScript)](manual/configuration/add-your-own-complex-modifications-js.md)
  - [Choose devices](manual/configuration/configure-devices.md)
  - [Disable the built-in keyboard when external keyboard is connected](manual/configuration/disable-built-in-keyboard.md)
  - [Set keyboard type](manual/configuration/configure-keyboard-type.md)
  - [Configure icon in menu bar](manual/configuration/configure-menu-bar-icon.md)
- [Operation](manual/operation.md)
  - [Quit](manual/operation/quit.md)
  - [Restart](manual/operation/restart.md)
  - [Uninstall](manual/operation/uninstall.md)
  - [Check for updates](manual/operation/check-for-updates.md)
  - [Confirm the result of configuration (EventViewer)](manual/operation/eventviewer.md)
  - [Manage profiles](manual/operation/profiles.md)
  - [Show log messages](manual/operation/log.md)
  - [Export and import configuration](manual/operation/export.md)
  - [About Unsafe Configuration](manual/operation/about-unsafe-configuration.md)
  - [Downgrade](manual/operation/downgrade.md)
- [Misc](manual/misc.md)
  - [Required macOS settings](manual/misc/required-macos-settings.md)
  - [About "Device is ignored temporarily" alert](manual/misc/ignored-temporarily.md)
  - [Implicit behavior](manual/misc/implicit-behavior.md)
  - [Input event modification chaining](manual/misc/event-modification-chaining.md)
  - [MultitouchExtension](manual/misc/multitouch-extension.md)
  - [Command line interface](manual/misc/command-line-interface.md)
  - [The location of the configuration file](manual/misc/configuration-file-path.md)
  - [Change app icon](manual/misc/change-app-icon.md)

### Help

- [Help](help.md)
- [Troubleshooting](help/troubleshooting.md)
  - [Breaking changes introduced by the version upgrade](help/troubleshooting/breaking-changes.md)
  - [Driver alert keeps showing up](help/troubleshooting/driver-alert-keeps-showing-up.md)
  - ["Fumihiko Takayama" is shown in Login Items](help/troubleshooting/fumihiko-takayama-in-login-items.md)
  - [Karabiner-Elements stopped working after macOS update](help/troubleshooting/stopped-working-after-macos-update.md)
  - [Touch Bar does not change to f1-f12 when I press the fn key](help/troubleshooting/touch-bar-function-keys.md)
  - [Control-eject shortcut does not work when Karabiner-Elements is running](help/troubleshooting/control-eject.md)
  - [Cannot use some three key combinations (key event is not fired)](help/troubleshooting/cannot-use-some-key-combination.md)
  - ["karabiner.json is not owned by a valid user" error message in log](help/troubleshooting/json-owner-is-invalid.md)
  - [Placeholder Developer is shown in Security & Privacy System Preferences](help/troubleshooting/placeholder-developer.md)
  - [Caps Lock LED not working](help/troubleshooting/caps-lock-led-not-working.md)
  - [Settings window is shown at login](help/troubleshooting/preferences-window-shown-at-login.md)
  - [Input symbols are different from the key code name on non-ANSI keyboards](help/troubleshooting/symbols-with-non-ansi-keyboard.md)
  - [Compatibility with Logitech Logi Options+: Fn keys](help/troubleshooting/logitech-logi-options-plus-compatibility.md)
- [How to](help/how-to.md)
  - [How to change mouse buttons](help/how-to/mouse-button.md)
  - [How to use sticky modifier keys](help/how-to/sticky-modifier-key.md)
  - [How to disable caps lock delay](help/how-to/disable-caps-lock-delay.md)
  - [Is it possible to adjust the key repeat rate?](help/how-to/key-repeat.md)
  - [How to disable running Karabiner-Elements at login](help/how-to/disable-open-at-login.md)
  - [How to use Karabiner-Elements on the password entry screen before logging in](help/how-to/use-before-logging-in.md)
  - [Details on changing to function keys](help/how-to/function-keys.md)
- [Advanced topics](help/advanced-topics.md)
  - [Installed files](help/advanced-topics/installed-files.md)
  - [Security](help/advanced-topics/security.md)
  - [Set environment variables](help/advanced-topics/set-environment-variables.md)
  - [Guide for supporting unsupported keys](help/advanced-topics/unknown-events.md)
  - [What is the lock indicator on Karabiner-Elements and Karabiner-EventViewer icon](help/advanced-topics/lock-icon.md)

### Karabiner Configuration Reference Manual

- [Karabiner Configuration Reference Manual](json.md)
- [File locations](json/location.md)
- [karabiner.json data structure](json/root-data-structure.md)
- [Typical complex_modifications examples](json/typical-complex-modifications-examples.md)
- [Expert complex_modifications examples](json/expert-complex-modifications-examples.md)
  - [Letter key holding modifier](json/expert-complex-modifications-examples/letter-key-holding-modifier.md)
  - [Letter key release order modifier](json/expert-complex-modifications-examples/letter-key-release-order-modifier.md)
  - [Swap fn and non-fn behavior for function keys on external keyboards](json/expert-complex-modifications-examples/swap-function-keys-on-external-keyboards.md)
- [complex_modifications manipulator evaluation priority](json/complex-modifications-manipulator-evaluation-priority.md)
- [complex_modifications manipulator definition](json/complex-modifications-manipulator-definition.md)
  - [from event definition](json/complex-modifications-manipulator-definition/from.md)
    - [from.any](json/complex-modifications-manipulator-definition/from/any.md)
    - [from.modifiers](json/complex-modifications-manipulator-definition/from/modifiers.md)
    - [from.integer_value](json/complex-modifications-manipulator-definition/from/integer-value.md)
    - [from.simultaneous](json/complex-modifications-manipulator-definition/from/simultaneous.md)
    - [from.simultaneous_options](json/complex-modifications-manipulator-definition/from/simultaneous-options.md)
  - [to event definition](json/complex-modifications-manipulator-definition/to.md)
    - [to.shell_command](json/complex-modifications-manipulator-definition/to/shell-command.md)
    - [to.select_input_source](json/complex-modifications-manipulator-definition/to/select-input-source.md)
    - [to.set_variable](json/complex-modifications-manipulator-definition/to/set-variable.md)
    - [to.set_notification_message](json/complex-modifications-manipulator-definition/to/set-notification-message.md)
    - [to.mouse_key](json/complex-modifications-manipulator-definition/to/mouse-key.md)
    - [to.sticky_modifier](json/complex-modifications-manipulator-definition/to/sticky-modifier.md)
    - [to.software_function](json/complex-modifications-manipulator-definition/to/software_function.md)
      - [cg_event_double_click](json/complex-modifications-manipulator-definition/to/software_function/cg_event_double_click.md)
      - [iokit_power_management_sleep_system](json/complex-modifications-manipulator-definition/to/software_function/iokit_power_management_sleep_system.md)
      - [open_application](json/complex-modifications-manipulator-definition/to/software_function/open_application.md)
      - [set_mouse_cursor_position](json/complex-modifications-manipulator-definition/to/software_function/set_mouse_cursor_position.md)
    - [to.send_user_command](json/complex-modifications-manipulator-definition/to/send-user-command.md)
    - [to.modifiers](json/complex-modifications-manipulator-definition/to/modifiers.md)
    - [to.from_event](json/complex-modifications-manipulator-definition/to/from-event.md)
    - [to.lazy](json/complex-modifications-manipulator-definition/to/lazy.md)
    - [to.repeat](json/complex-modifications-manipulator-definition/to/repeat.md)
    - [to.halt](json/complex-modifications-manipulator-definition/to/halt.md)
    - [to.hold_down_milliseconds](json/complex-modifications-manipulator-definition/to/hold-down-milliseconds.md)
    - [to.conditions](json/complex-modifications-manipulator-definition/to/to-conditions.md)
  - [to_if_alone](json/complex-modifications-manipulator-definition/to-if-alone.md)
  - [to_if_held_down](json/complex-modifications-manipulator-definition/to-if-held-down.md)
  - [to_if_other_key_pressed](json/complex-modifications-manipulator-definition/to-if-other-key-pressed.md)
  - [to_after_key_up](json/complex-modifications-manipulator-definition/to-after-key-up.md)
  - [to_delayed_action](json/complex-modifications-manipulator-definition/to-delayed-action.md)
  - [Conditions](json/complex-modifications-manipulator-definition/conditions.md)
    - [frontmost_application_if, frontmost_application_unless](json/complex-modifications-manipulator-definition/conditions/frontmost-application.md)
    - [device_if, device_unless, device_exists_if, device_exists_unless](json/complex-modifications-manipulator-definition/conditions/device.md)
    - [keyboard_type_if, keyboard_type_unless](json/complex-modifications-manipulator-definition/conditions/keyboard-type.md)
    - [input_source_if, input_source_unless](json/complex-modifications-manipulator-definition/conditions/input-source.md)
    - [variable_if, variable_unless](json/complex-modifications-manipulator-definition/conditions/variable.md)
    - [expression_if, expression_unless](json/complex-modifications-manipulator-definition/conditions/expression.md)
    - [event_changed_if, event_changed_unless](json/complex-modifications-manipulator-definition/conditions/event-changed.md)
  - [Other types](json/complex-modifications-manipulator-definition/other-types.md)
    - [mouse_basic](json/complex-modifications-manipulator-definition/other-types/mouse-basic.md)
    - [mouse_motion_to_scroll](json/complex-modifications-manipulator-definition/other-types/mouse-motion-to-scroll.md)
- [Extra documents](json/extra.md)
  - [MultitouchExtension integration](json/extra/multitouch-extension.md)
  - [Virtual modifier](json/extra/virtual-modifier.md)
- [External JSON generators](json/external-json-generators.md)

### Release And Site Information

- [Release notes](releasenotes.md)
- [Privacy](privacy.md)
- [Contact](contact.md)
- [Pricing](pricing.md)

## Lookup

1. Find the relevant section in Contents above.
2. Read that file with the Read tool.
3. If the answer spans UI setup and JSON behavior, read both the Manual and Karabiner Configuration Reference Manual pages.
4. For remapping examples, start with `json/typical-complex-modifications-examples.md`, then inspect the linked `from`, `to`, and `conditions` reference pages.
