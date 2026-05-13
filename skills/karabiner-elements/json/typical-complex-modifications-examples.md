# Typical complex_modifications examples
## Swap ; and :
- Equal to swap ; and shift-; : from.modifiers
```
{

    
"description"
:
 
"Swap ; and :"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"semicolon"
,

                
"modifiers"
:
 
{

                    
"mandatory"
:
 
[
"shift"
],

                    
"optional"
:
 
[
"caps_lock"
]

                
}

            
},

            
"to"
:
 
[{
 
"key_code"
:
 
"semicolon"
 
}]

        
},

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"semicolon"
,

                
"modifiers"
:
 
{

                    
"optional"
:
 
[
"caps_lock"
]

                
}

            
},

            
"to"
:
 
[{
 
"key_code"
:
 
"semicolon"
,
 
"modifiers"
:
 
[
"left_shift"
]
 
}]

        
}

    
]

}
```
## Change control-h to delete
- Change control-h to delete : from.modifiers
- Change control-option-h to option-delete .
```
{

    
"description"
:
 
"Change control-h to delete"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"h"
,

                
"modifiers"
:
 
{

                    
"mandatory"
:
 
[
"control"
],

                    
"optional"
:
 
[
"caps_lock"
,
 
"option"
]

                
}

            
},

            
"to"
:
 
[{
 
"key_code"
:
 
"delete_or_backspace"
 
}]

        
}

    
]

}
```
## Change mouse button4 and button5 to back and forward
Change mouse button 4 and button 5 to [ + left_arrow and ] + right_arrow .
To use this configuration, you need to enable your mouse in the Devices tab .
```
{

    
"description"
:
 
"Change mouse button4 and button5 to back and forward"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{
 
"pointing_button"
:
 
"button4"
 
},

            
"to"
:
 
[

                
{

                    
"key_code"
:
 
"open_bracket"
,

                    
"modifiers"
:
 
[
"left_command"
]

                
}

            
]

        
},

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{
 
"pointing_button"
:
 
"button5"
 
},

            
"to"
:
 
[

                
{

                    
"key_code"
:
 
"close_bracket"
,

                    
"modifiers"
:
 
[
"left_command"
]

                
}

            
]

        
}

    
]

}
```
If the virtual keyboard type is set to something other than ANSI, you need to adjust the key codes to match that keyboard type.
For example, if it is set to JIS, buttons must be configured as follows:
- Change button4 to left_command + close_bracket
- Change button5 to left_command + backslash
See key code mappings .
## Change caps_lock to escape on the built-in keyboard
- An example of using modifiers.optional == [“any”]: from.modifiers
- Device-specific rule: device_if, device_unless, device_exists_if, device_exists_unless
```
{

    
"description"
:
 
"Change caps_lock to escape on the built-in keyboard"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"caps_lock"
,

                
"modifiers"
:
 
{

                    
"optional"
:
 
[
"any"
]

                
}

            
},

            
"to"
:
 
[{
 
"key_code"
:
 
"escape"
 
}],

            
"conditions"
:
 
[

                
{

                    
"type"
:
 
"device_if"
,

                    
"identifiers"
:
 
[{
 
"is_built_in_keyboard"
:
 
true
 
}]

                
}

            
]

        
}

    
]

}
```
## Change left_command+3 -> 2, left_shift+3 -> @ on the built-in keyboard
- An example of using modifiers.optional == [“any”] with modifiers.mandatory: from.modifiers
- Device-specific rule: device_if, device_unless, device_exists_if, device_exists_unless
```
{

    
"description"
:
 
"Change left_command+3 -> 2, left_shift+3 -> @ on the built-in keyboard"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"3"
,

                
"modifiers"
:
 
{

                    
"mandatory"
:
 
[
"left_command"
],

                    
"optional"
:
 
[
"any"
]

                
}

            
},

            
"to"
:
 
[{
 
"key_code"
:
 
"2"
 
}],

            
"conditions"
:
 
[

                
{

                    
"type"
:
 
"device_if"
,

                    
"identifiers"
:
 
[{
 
"is_built_in_keyboard"
:
 
true
 
}]

                
}

            
]

        
},

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"3"
,

                
"modifiers"
:
 
{

                    
"mandatory"
:
 
[
"left_shift"
],

                    
"optional"
:
 
[
"any"
]

                
}

            
},

            
"to"
:
 
[{
 
"key_code"
:
 
"2"
,
 
"modifiers"
:
 
[
"left_shift"
]
 
}],

            
"conditions"
:
 
[

                
{

                    
"type"
:
 
"device_if"
,

                    
"identifiers"
:
 
[{
 
"is_built_in_keyboard"
:
 
true
 
}]

                
}

            
]

        
}

    
]

}
```
## Open files in Finder using the return key
In this configuration, the return key remains unchanged during text input (e.g., when renaming files or performing a search) by checking accessibility.focused_ui_element.role_string .
- Use a system-provided variable: expression_if, expression_unless
- Application-specific rule: frontmost_application_if, frontmost_application_unless
```
{

    
"description"
:
 
"Open files in Finder using the return key"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"return_or_enter"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"caps_lock"
]
 
}

            
},

            
"to"
:
 
[

                
{

                    
"key_code"
:
 
"o"
,

                    
"modifiers"
:
 
[
"left_command"
]

                
}

            
],

            
"conditions"
:
 
[

                
{

                    
"type"
:
 
"frontmost_application_if"
,

                    
"bundle_identifiers"
:
 
[
"^com\\.apple\\.finder$"
]

                
},

                
{

                    
"type"
:
 
"expression_unless"
,

                    
"expression"
:
 
"accessibility.focused_ui_element.role_string like 'AXText*'"

                
}

            
]

        
}

    
]

}
```
## Disable command-l in Finder
- Application-specific rule: frontmost_application_if, frontmost_application_unless
```
{

    
"description"
:
 
"Disable command-l in Finder"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"l"
,

                
"modifiers"
:
 
{

                    
"mandatory"
:
 
[
"command"
],

                    
"optional"
:
 
[
"caps_lock"
]

                
}

            
},

            
"conditions"
:
 
[

                
{

                    
"type"
:
 
"frontmost_application_if"
,

                    
"bundle_identifiers"
:
 
[
"^com\\.apple\\.finder$"
]

                
}

            
]

        
}

    
]

}
```
## Post escape if left_control is pressed alone
- Post events when a key is pressed alone: to_if_alone
- Post events when a key is held down: to_if_held_down
- The lazy modifier: to.lazy
```
{

    
"description"
:
 
"Post escape if left_control is tapped"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"left_control"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[

                
{

                    
"key_code"
:
 
"left_control"
,

                    
"lazy"
:
 
true

                
}

            
],

            
"to_if_alone"
:
 
[{
 
"key_code"
:
 
"escape"
 
}],

            
"to_if_held_down"
:
 
[{
 
"key_code"
:
 
"left_control"
 
}],

            
"parameters"
:
 
{

                
"basic.to_if_alone_timeout_milliseconds"
:
 
100
,

                
"basic.to_if_held_down_threshold_milliseconds"
:
 
100

            
}

        
}

    
]

}
```
This uses "lazy": true to prevent left_control from being sent immediately after the key is pressed. Instead, it explicitly sends left_control using to_if_held_down when the key is held down for a short period.
## Open Safari if escape is held down
- Post events when a key is pressed alone: to_if_alone
- Post events when a key is held down: to_if_held_down
- Open an application: open_application
```
{

    
"description"
:
 
"Open Safari if escape is held down"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"escape"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"caps_lock"
]
 
}

            
},

            
"parameters"
:
 
{

                
"basic.to_if_alone_timeout_milliseconds"
:
 
250
,

                
"basic.to_if_held_down_threshold_milliseconds"
:
 
250

            
},

            
"to_if_alone"
:
 
[{
 
"key_code"
:
 
"escape"
 
}],

            
"to_if_held_down"
:
 
[

                
{

                    
"software_function"
:
 
{

                        
"open_application"
:
 
{

                            
"bundle_identifier"
:
 
"com.apple.Safari"

                        
}

                    
}

                
}

            
]

        
}

    
]

}
```
## Paste (command+v) if escape is held down
- Post events when a key is pressed alone: to_if_alone
- Post events when a key is held down: to_if_held_down
```
{

    
"description"
:
 
"Paste (command+v) if escape is held down"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"escape"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"parameters"
:
 
{

                
"basic.to_if_alone_timeout_milliseconds"
:
 
250
,

                
"basic.to_if_held_down_threshold_milliseconds"
:
 
250

            
},

            
"to_if_alone"
:
 
[{
 
"key_code"
:
 
"escape"
 
}],

            
"to_if_held_down"
:
 
[

                
{

                    
"key_code"
:
 
"v"
,

                    
"modifiers"
:
 
[
"left_command"
],

                    
"repeat"
:
 
false

                
}

            
]

        
}

    
]

}
```
## Change option+tab to command+tab
```
{

    
"description"
:
 
"Change option+tab to command+tab"
,

    
"manipulators"
:
 
[

        
// Change left_option to left_command if tab key is pressed together.

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"left_option"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[{
 
"key_code"
:
 
"left_option"
 
}],

            
"to_if_other_key_pressed"
:
 
[

                
{

                    
"other_keys"
:
 
[

                        
{

                            
"key_code"
:
 
"tab"
,

                            
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

                        
}

                    
],

                    
"to"
:
 
[

                        
{

                            
"key_code"
:
 
"left_command"

                        
}

                    
]

                
}

            
]

        
},

        
// Change right_option to right_command if tab key is pressed together.

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"right_option"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[{
 
"key_code"
:
 
"right_option"
 
}],

            
"to_if_other_key_pressed"
:
 
[

                
{

                    
"other_keys"
:
 
[

                        
{

                            
"key_code"
:
 
"tab"
,

                            
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

                        
}

                    
],

                    
"to"
:
 
[

                        
{

                            
"key_code"
:
 
"right_command"

                        
}

                    
]

                
}

            
]

        
}

    
]

}
```
## Change right_shift x2 to mission_control (new style)
This example is available since Karabiner-Elements 15.5.19.
- Use variable: expression_if, expression_unless to.set_variable
- to_delayed_action
```
{

    
"description"
:
 
"Change right_shift x2 to mission_control (new style)"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"right_shift"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[

                
{
 
"apple_vendor_keyboard_key_code"
:
 
"mission_control"
 
},

                
{
 
"key_code"
:
 
"vk_none"
 
}

            
],

            
"conditions"
:
 
[

                
{

                    
"type"
:
 
"expression_if"
,

                    
"expression"
:
 
"right_shift_x2_expiration > system.now.milliseconds"

                
}

            
]

        
},

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"right_shift"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[

                
{

                    
"set_variable"
:
 
{

                        
"name"
:
 
"right_shift_x2_expiration"
,

                        
"expression"
:
 
"system.now.milliseconds + 300"

                    
}

                
},

                
{
 
"key_code"
:
 
"right_shift"
 
}

            
]

        
}

    
]

}
```
## Change right_shift x2 to mission_control (old style)
- Use variable: variable_if, variable_unless to.set_variable
- to_delayed_action
```
{

    
"description"
:
 
"Change right_shift x2 to mission_control (old style)"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"right_shift"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[

                
{
 
"apple_vendor_keyboard_key_code"
:
 
"mission_control"
 
},

                
{
 
"key_code"
:
 
"vk_none"
 
}

            
],

            
"conditions"
:
 
[

                
{

                    
"type"
:
 
"variable_if"
,

                    
"name"
:
 
"right_shift pressed"
,

                    
"value"
:
 
1

                
}

            
]

        
},

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"right_shift"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[

                
{

                    
"set_variable"
:
 
{

                        
"name"
:
 
"right_shift pressed"
,

                        
"value"
:
 
1

                    
}

                
},

                
{
 
"key_code"
:
 
"right_shift"
 
}

            
],

            
"to_delayed_action"
:
 
{

                
"to_if_invoked"
:
 
[

                    
{

                        
"set_variable"
:
 
{

                            
"name"
:
 
"right_shift pressed"
,

                            
"value"
:
 
0

                        
}

                    
}

                
],

                
"to_if_canceled"
:
 
[

                    
{

                        
"set_variable"
:
 
{

                            
"name"
:
 
"right_shift pressed"
,

                            
"value"
:
 
0

                        
}

                    
}

                
]

            
}

        
}

    
]

}
```
## Change double press of q to escape
This example is available since Karabiner-Elements 15.3.7.
- Use variable: variable_if, variable_unless to.set_variable
- to_delayed_action
```
{

    
"description"
:
 
"Change double press of q to escape"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"q"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[

                
{
 
"set_variable"
:
 
{
 
"name"
:
 
"q pressed"
,
 
"value"
:
 
false
 
}
 
},

                
{
 
"key_code"
:
 
"escape"
 
}

            
],

            
"conditions"
:
 
[

                
{
 
"type"
:
 
"variable_if"
,
 
"name"
:
 
"q pressed"
,
 
"value"
:
 
true
 
}

            
]

        
},

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"q"
,

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[{
 
"set_variable"
:
 
{
 
"name"
:
 
"q pressed"
,
 
"value"
:
 
true
 
}
 
}],

            
"to_delayed_action"
:
 
{

                
"to_if_invoked"
:
 
[

                    
{

                        
"key_code"
:
 
"q"
,

                        
"conditions"
:
 
[

                            
{

                                
"type"
:
 
"variable_if"
,

                                
"name"
:
 
"q pressed"
,

                                
"value"
:
 
true

                            
}

                        
]

                    
},

                    
{
 
"set_variable"
:
 
{
 
"name"
:
 
"q pressed"
,
 
"value"
:
 
false
 
}
 
}

                
],

                
"to_if_canceled"
:
 
[

                    
{

                        
"key_code"
:
 
"q"
,

                        
"conditions"
:
 
[

                            
{

                                
"type"
:
 
"variable_if"
,

                                
"name"
:
 
"q pressed"
,

                                
"value"
:
 
true

                            
}

                        
]

                    
},

                    
{
 
"set_variable"
:
 
{
 
"name"
:
 
"q pressed"
,
 
"value"
:
 
false
 
}
 
}

                
]

            
}

        
}

    
]

}
```
## Change equal+delete to forward_delete if these keys are pressed simultaneously
- from.simultaneous
```
{

    
"description"
:
 
"Change equal+delete to forward_delete if these keys are pressed simultaneously"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"simultaneous"
:
 
[

                    
{
 
"key_code"
:
 
"equal_sign"
 
},

                    
{
 
"key_code"
:
 
"delete_or_backspace"
 
}

                
],

                
"modifiers"
:
 
{
 
"optional"
:
 
[
"any"
]
 
}

            
},

            
"to"
:
 
[{
 
"key_code"
:
 
"delete_forward"
 
}]

        
}

    
]

}
```
## Input Unicode characters via the clipboard
- to.hold_down_milliseconds
With this setting, pressing fn + x copies ✅🆗 to the clipboard and then pastes it.
```
{

    
"description"
:
 
"Input ✅🆗 by fn+x"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"x"
,

                
"modifiers"
:
 
{

                    
"mandatory"
:
 
[
"fn"
]

                
}

            
},

            
"to"
:
 
[

                
{

                    
"shell_command"
:
 
"/bin/echo -n '✅🆗' | LANG=en_US.UTF-8 /usr/bin/pbcopy"
,

                    
"hold_down_milliseconds"
:
 
200

                
},

                
{

                    
"key_code"
:
 
"v"
,

                    
"modifiers"
:
 
[
"left_command"
]

                
}

            
]

        
}

    
]

}
```
The key point is to specify LANG when running pbcopy. If you don’t, the string won’t be copied correctly.
## Input Unicode characters using Unicode Hex Input
- to.select_input_source
In this setting, fn + d changes the Input Source to Unicode Hex Input and inputs ✅ (U+2705). Therefore, you need to enable Unicode Hex Input in Input Source settings .
```
{

    
"description"
:
 
"Input ✅ by fn+d"
,

    
"manipulators"
:
 
[

        
{

            
"type"
:
 
"basic"
,

            
"from"
:
 
{

                
"key_code"
:
 
"d"
,

                
"modifiers"
:
 
{

                    
"mandatory"
:
 
[
"fn"
]

                
}

            
},

            
"to"
:
 
[

                
{

                    
"select_input_source"
:
 
{

                        
"input_source_id"
:
 
"com.apple.keylayout.UnicodeHexInput"

                    
},

                    
"hold_down_milliseconds"
:
 
200

                
},

                
{

                    
"key_code"
:
 
"2"
,

                    
"modifiers"
:
 
[
"left_option"
]

                
},

                
{

                    
"key_code"
:
 
"7"
,

                    
"modifiers"
:
 
[
"left_option"
]

                
},

                
{

                    
"key_code"
:
 
"0"
,

                    
"modifiers"
:
 
[
"left_option"
]

                
},

                
{

                    
"key_code"
:
 
"5"
,

                    
"modifiers"
:
 
[
"left_option"
]

                
},

                
{

                    
"select_input_source"
:
 
{
 
"language"
:
 
"en"
 
}

                
}

            
]

        
}

    
]

}
```