# Letter key release order modifier
Holding down v and pressing j or k enters arrow mode.
- v (hold) + j : down arrow
- v (hold) + k : up arrow
- You need to keep holding down the v and j or k keys, or release the j or k key to enter arrow mode.
- If you release the v key first, vj or vk will be typed as normal characters.
## JavaScript version
```
// JavaScript must be written in ECMAScript 5.1.

function
 
main
()
 
{

    
const
 
definitions
 
=
 
[

        
{
 
from
:
 
'j'
,
 
to
:
 
'down_arrow'
 
},

        
{
 
from
:
 
'k'
,
 
to
:
 
'up_arrow'
 
},

    
]

    
const
 
manipulators
 
=
 
[]

    
definitions
.
forEach
(
function
 
(
def
)
 
{

        
manipulators
.
push
({

            
type
:
 
'basic'
,

            
from
:
 
{

                
key_code
:
 
def
.
from
,

                
modifiers
:
 
{
 
optional
:
 
[
'any'
]
 
},

            
},

            
to
:
 
[{
 
key_code
:
 
def
.
to
 
}],

            
conditions
:
 
[{
 
type
:
 
'variable_if'
,
 
name
:
 
'v_flag'
,
 
value
:
 
true
 
}],

        
})

        
manipulators
.
push
({

            
type
:
 
'basic'
,

            
from
:
 
{

                
simultaneous
:
 
[{
 
key_code
:
 
'v'
 
},
 
{
 
key_code
:
 
def
.
from
 
}],

                
simultaneous_options
:
 
{

                    
key_down_order
:
 
'strict'
,

                    
key_up_order
:
 
'strict_inverse'
,

                    
to_after_key_up
:
 
[

                        
{
 
set_variable
:
 
{
 
name
:
 
'v_flag'
,
 
value
:
 
false
 
}
 
},

                    
],

                
},

                
modifiers
:
 
{
 
optional
:
 
[
'any'
]
 
},

            
},

            
to
:
 
[

                
{
 
set_variable
:
 
{
 
name
:
 
'v_flag'
,
 
value
:
 
true
 
}
 
},

                
{
 
key_code
:
 
def
.
to
 
},

            
],

            
parameters
:
 
{

                
'basic.simultaneous_threshold_milliseconds'
:
 
500
,

            
},

        
})

    
})

    
return
 
{

        
description
:
 
'Holding down v and pressing j,k enters arrow mode'
,

        
manipulators
:
 
manipulators
,

    
}

}

main
()
```
## JSON version
```
{

    
"description"
:
 
"Holding down v and pressing j,k enters arrow mode"
,

    
"manipulators"
:
 
[

        
//

        
// v+j

        
//

        
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
 
"j"
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
 
"down_arrow"
 
}],

            
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
 
"v_flag"
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

                
"simultaneous"
:
 
[{
 
"key_code"
:
 
"v"
 
},
 
{
 
"key_code"
:
 
"j"
 
}],

                
"simultaneous_options"
:
 
{

                    
"key_down_order"
:
 
"strict"
,

                    
"key_up_order"
:
 
"strict_inverse"
,

                    
"to_after_key_up"
:
 
[

                        
{
 
"set_variable"
:
 
{
 
"name"
:
 
"v_flag"
,
 
"value"
:
 
false
 
}
 
}

                    
]

                
},

                
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
 
"v_flag"
,
 
"value"
:
 
true
 
}
 
},

                
{
 
"key_code"
:
 
"down_arrow"
 
}

            
],

            
"parameters"
:
 
{

                
"basic.simultaneous_threshold_milliseconds"
:
 
500

            
}

        
},

        
//

        
// v+k

        
//

        
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
 
"k"
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
 
"up_arrow"
 
}],

            
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
 
"v_flag"
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

                
"simultaneous"
:
 
[{
 
"key_code"
:
 
"v"
 
},
 
{
 
"key_code"
:
 
"k"
 
}],

                
"simultaneous_options"
:
 
{

                    
"key_down_order"
:
 
"strict"
,

                    
"key_up_order"
:
 
"strict_inverse"
,

                    
"to_after_key_up"
:
 
[

                        
{
 
"set_variable"
:
 
{
 
"name"
:
 
"v_flag"
,
 
"value"
:
 
false
 
}
 
}

                    
]

                
},

                
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
 
"v_flag"
,
 
"value"
:
 
true
 
}
 
},

                
{
 
"key_code"
:
 
"up_arrow"
 
}

            
],

            
"parameters"
:
 
{

                
"basic.simultaneous_threshold_milliseconds"
:
 
500

            
}

        
}

    
]

}
```