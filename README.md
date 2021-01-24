# domgw
Domotic gateway for our home

This software written in python listens into the rabbitmq "minetest_gw" queue and execute command messages for domotic.

## Chat message
'''json
{
  "typ":"chat",
  "dst":"<Destination player>",
  "msg":"<Message sent from the minetest game>"
}
'''
  
## Cat tower command message
This message commands the "minou cat" tower LEDs.
  - 26 LEDs (from 0 to 25) are on the tower roof
  - 8 LEDs (from 26 to 33) are into the tower
  
It is decoded by the software and a http request is issued to the local network of our home to the arduino server that controls the tower.
  
'''json
{
  "typ":"tour",
  "num_start":<LED start index>,
  "num_end":<LED end index>,
  "col":<LED color to apply>
}
'''
  
**Colors are:**
- "r" : Red
- "g" : Green
- "b" : Blue
- "w" : White
- "0" : Black (Zero)
- ...

***NB:*** See the arduino cattower project for more details. 

## Hue Message

The Hue message give the command order to the hue lights of our home

'''json
{
  "typ":"hue",
  "nam":"<Name of the hue light / Same as Philips application>",
  "cmd":"<Command to send>"
}
'''

The commands are "on" or "off".
