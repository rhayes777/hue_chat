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


# Set the model and prompt
model_engine = "text-davinci-003"
prompt = """
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

I want responses to be in the form of a JSON with keys "hue", "saturation" and "brightness".

Give me the JSON for baby blue. 

"""

# Set the maximum number of tokens to generate in the response
max_tokens = 1024

# Generate a response
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=0.1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

response = completion.choices[0].text
# Print the response
print(response)

bridge = get_bridge()

light = bridge.lights[0]

for key, value in json.loads(response).items():
    setattr(light, key, value)
