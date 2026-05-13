# complex_modifications manipulator definition
```
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
...
},

        
"to"
:
 
[
...
],

        
"to_if_alone"
:
 
[
...
],

        
"to_if_held_down"
:
 
[
...
],

        
"to_if_other_key_pressed"
:
 
[
...
],

        
"to_after_key_up"
:
 
[
...
],

        
"to_delayed_action"
:
 
{

            
"to_if_invoked"
:
 
[
...
],

            
"to_if_canceled"
:
 
[
...
],

        
},

        
"conditions"
:
 
[
...
],

        
"parameters"
:
 
{
...
},

        
"description"
:
 
"Optional description for human"

    
},

    
...

]
```
| Name | Required | Description |
| --- | --- | --- |
| type | Required | "basic" is specified |
| from | Required | The name of key code, consumer key code or pointing button which you want to change |
| to | Optional | Events which are sent when you press from key |
| to_if_alone | Optional | Events which are sent when you press from key alone |
| to_if_held_down | Optional | Events which are sent when you hold down from key |
| to_if_other_key_pressed | Optional | Events which are sent when you press other keys with from key |
| to_after_key_up | Optional | Events which are sent after you release from key |
| to_delayed_action | Optional | Events which are sent after 500 milliseconds at you press from key |
| conditions | Optional | Manipulator is applied only if condition is matched (e.g., the frontmost application) |
| parameters | Optional | Override parameters such as to_if_alone_timeout_milliseconds |
| description | Optional | A human-readable comment |
## Detail
- from event definition
- to event definition
- to_if_alone
- to_if_held_down
- to_if_other_key_pressed
- to_after_key_up
- to_delayed_action
- conditions
## Other manipulators
Manipulators which type is not "basic" .
- mouse_basic
- mouse_motion_to_scroll
## Table of Contents
- from event definition from.any from.modifiers from.integer_value from.simultaneous from.simultaneous_options
- to event definition to.shell_command to.select_input_source to.set_variable to.set_notification_message to.mouse_key to.sticky_modifier to.software_function cg_event_double_click iokit_power_management_sleep_system open_application set_mouse_cursor_position to.send_user_command to.modifiers to.from_event to.lazy to.repeat to.halt to.hold_down_milliseconds to.conditions
- to_if_alone
- to_if_held_down
- to_if_other_key_pressed
- to_after_key_up
- to_delayed_action
- Conditions frontmost_application_if, frontmost_application_unless device_if, device_unless, device_exists_if, device_exists_unless keyboard_type_if, keyboard_type_unless input_source_if, input_source_unless variable_if, variable_unless expression_if, expression_unless event_changed_if, event_changed_unless
- Other types mouse_basic mouse_motion_to_scroll