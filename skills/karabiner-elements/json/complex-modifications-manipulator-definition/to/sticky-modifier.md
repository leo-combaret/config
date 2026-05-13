# to.sticky_modifier
sticky_modifier changes a key to a sticky modifier key.
## Examples
```
{

    
"description"
:
 
"Change right_shift to sticky modifier"
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
 
[{
 
"key_code"
:
 
"right_shift"
 
}],

            
"to_if_alone"
:
 
[{
 
"sticky_modifier"
:
 
{
 
"right_shift"
:
 
"toggle"
 
}
 
}]

        
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

            
"sticky_modifier"
:
 
{

                
"{modifier_name}"
:
 
"on | off | toggle"

            
}

        
}

    
]

}
```
| Name | Required | Description |
| --- | --- | --- |
| {modifier_name} | Optional | - on always activates a sticky modifier. - off is vice versa. - toggle toggles a sticky modifier. toggle is suitable for most cases. |
## Supported modifiers
- left_control
- left_shift
- left_option
- left_command
- right_control
- right_shift
- right_option
- right_command
- fn
You have to specify only one modifier.
If you want to activate multiple sticky modifiers, put multiple sticky_modifier as follows.
```
{

    
"to"
:
 
[

        
{

            
"sticky_modifier"
:
 
{

                
"left_control"
:
 
"toggle"

            
}

        
},

        
{

            
"sticky_modifier"
:
 
{

                
"left_shift"
:
 
"toggle"

            
}

        
}

    
]

}
```