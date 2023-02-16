import json
import os
import time
from pathlib import Path

import discoverhue
import openai
import phue

openai.api_key = os.environ["OPENAI_API_KEY"]


def find_ip():
    bridges = discoverhue.find_bridges()
    url = list(bridges.values())[0]
    return url.split(":")[1].strip("/")


def get_ip():
    ip_file_path = Path.home() / ".ip.txt"
    if ip_file_path.exists():
        return ip_file_path.read_text()
    else:
        ip = find_ip()
        ip_file_path.write_text(ip)
        return ip


def get_bridge():
    while True:
        try:
            return phue.Bridge(get_ip())
        except phue.PhueRegistrationException:
            print("Press the button on the bridge")
            time.sleep(2)


header = """
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
The light ids are 0 and 1. The color relates a key "color" to a dictionary with the keys "hue", "saturation" and "brightness". 

Give me a list of JSONs to configure the lights as I describe below. Give only the JSON and no additional characters.
"""


class ChatBot:
    def __init__(
            self,
            engine="text-davinci-003",
            max_tokens=1024,
            temperature=0.1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            header="",
    ):
        self.engine = engine
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

        self.header = header

        self._messages = []

    def __call__(self, message):
        self._messages.append(message)
        message = "\n".join(self._messages)
        prompt = f"{self.header}\n{message}"
        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
        ).choices[0].text.strip(" .\t\n")
        print(response)
        return json.loads(response)


bot = ChatBot(header=header)

response = bot("I want the lights to be red and green")

bridge = get_bridge()

for command in response:
    light_id = command["light_id"]
    color = command["color"]
    light = bridge.lights[light_id]
    for key, value in color.items():
        setattr(light, key, value)
