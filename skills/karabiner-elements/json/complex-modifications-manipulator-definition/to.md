# to event definition
```
{

    
"key_code"
:
 
"The name of key_code"
,

    
"consumer_key_code"
:
 
"The name of consumer_key_code"
,

    
"pointing_button"
:
 
"The name of pointing_button"
,

    
"shell_command"
:
 
"shell command"
,

    
"select_input_source"
:
 
{

        
"language"
:
 
"language regex"
,

        
"input_source_id"
:
 
"input source id regex"
,

        
"input_mode_id"
:
 
"input mode id regex"

    
},

    
"set_variable"
:
 
{

        
"name"
:
 
"variable name"
,

        
"value"
:
 
"variable value"

    
},

    
"mouse_key"
:
 
mouse_key
 
definition
,

    
"sticky_modifier"
:
 
sticky
 
modifier
 
definition
,

    
"software_function"
:
 
software
 
function
 
definition
,

    
"modifiers"
:
 
[

        
modifier
,

        
modifier
,

        
...

    
],

    
"from_event"
:
 
true
,

    
"lazy"
:
 
false
,

    
"repeat"
:
 
true
,

    
"halt"
:
 
false
,

    
"hold_down_milliseconds"
:
 
0
,

    
"conditions"
:
 
[
...
]

}
```
The following keys are exclusive. You cannot specify multiple items into one to entry.
- key_code
- consumer_key_code
- pointing_button
- shell_command
- select_input_source
- set_variable
- mouse_key
- sticky_modifier
- software_function ( software_function is available since Karabiner-Elements v13.5.1)
| Name | Required | Description |
| --- | --- | --- |
| key_code | Optional | Key code which you want to post |
| consumer_key_code | Optional | Consumer key code (media key code) which you want to post |
| pointing_button | Optional | Pointing button name which you want to post |
| shell_command | Optional | Shell command which you want to execute |
| select_input_source | Optional | Input source which you want to switch |
| set_variable | Optional | A varaible name and value which you want to change |
| mouse_key | Optional | A mouse key definition |
| sticky_modifier | Optional | A sticky modifier key definition |
| software_function | Optional | A software function definition |
| modifiers | Optional | Modifiers which are post with the event |
| from_event | Optional | Send the key or button specified in from |
| lazy | Optional | Lazy modifier flag |
| repeat | Optional | Key repeat flag |
| halt | Optional | A flag for to_after_key_up |
| hold_down_milliseconds | Optional | Interval of key_down and key_up when these events are sent at the same time |
| conditions | Optional | The event is transmitted only when the conditions are satisfied (e.g., variable_if) |
## Investigate key names
- You can find key_code , consumer_key_code and pointing_button names by EventViewer .
- You can also confirm names in list . (See "data" in the list.)
You can also specify key_code , consumer_key_code , pointing_button with raw number as follows.
```
{

    
"to"
:
 
[

        
{

            
"key_code"
:
 
41

        
}

    
]

}
```
Normally, a corresponding key_down event is sent when a key is pressed, and a key_up event is sent when it is released.
However, for certain keys, you might want both key_down and key_up to be sent when the key is pressed. For example, the mission_control key closes Mission Control on key_up, so if you press and hold the key and then release it, the Mission Control window you just opened will end up closing.
In such cases, you can send both key_down and key_up when the key is pressed by adding vk_none . In this scenario, no event will be triggered when the key is released.
```
{

    
"description"
:
 
"Open Mission Control by right_command + e"
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
 
"e"
,

                
"modifiers"
:
 
{

                    
"mandatory"
:
 
[
"right_command"
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

            
]

        
}

    
]

}
```
## Table of Contents
- to.shell_command
- to.select_input_source
- to.set_variable
- to.set_notification_message
- to.mouse_key
- to.sticky_modifier
- to.software_function cg_event_double_click iokit_power_management_sleep_system open_application set_mouse_cursor_position
- to.send_user_command
- to.modifiers
- to.from_event
- to.lazy
- to.repeat
- to.halt
- to.hold_down_milliseconds
- to.conditions