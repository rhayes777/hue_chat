#!/usr/bin/env python
from json import JSONDecodeError

from chat_bot import ChatBot
from hue import get_bridge

HEADER = """
I have a hue scale from 0 to 65535. 
red is 0.0
orange is 7281
yellow is 14563
purple is 50971
pink is 54612
green is 23665
blue is 43690

Saturation is from 0 to 254
Brightness is from 0 to 254

Two JSONs should be returned in a list. Each JSON should contain a color and a light_id. 
The light ids are 0 and 1. 
The color relates a key "color" to a dictionary with the keys "hue", "saturation" and "brightness". 

Give me a list of JSONs to configure the lights in response to the instructions below. 
Give only the JSON and no additional characters. 
Do not attempt to complete the instruction that I give.
Only give one JSON for each light. 
"""

bot = ChatBot(header=HEADER)
bridge = get_bridge()

while True:
    try:
        response = bot(input("What should I do with the lights? "))
    except JSONDecodeError:
        print("Oops something went wrong. Try again.")
        continue

    for command in response:
        light_id = command["light_id"]
        color = command["color"]
        light = bridge.lights[light_id]
        for key, value in color.items():
            setattr(light, key, value)
