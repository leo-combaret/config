# to.set_notification_message
set_notification_message sets or remove the notification message.
## Examples
Show the notification message while you press right shift key.
```
{

    
"description"
:
 
"Show a message while right_shift is pressed"
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

                    
// Show the notification message

                    
"set_notification_message"
:
 
{

                        
"id"
:
 
"my_message"
,

                        
"text"
:
 
"Hello World!"

                    
}

                
},

                
{

                    
"key_code"
:
 
"right_shift"

                
}

            
],

            
"to_after_key_up"
:
 
[

                
{

                    
// Hide the notification message

                    
"set_notification_message"
:
 
{

                        
"id"
:
 
"my_message"
,

                        
"text"
:
 
""

                    
}

                
}

            
]

        
}

    
]

}
```
## Specification
```
{

    
"to"
:
 
[

        
{

            
"set_notification_message"
:
 
{

                
"id"
:
 
"identifier of the message"
,

                
"text"
:
 
"message text"

            
}

        
}

    
]

}
```
| Name | Required | Description |
| --- | --- | --- |
| id | Required | Specify an unique string for your notification message |
| text | Required | Message body |
Do not forget to remove the notification message.
Set empty string to text to remove the notification message.