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
prompt = "Give me the value of hue from 0 to 65535 which corresponds to turquoise. Answer only with the number."

# Set the maximum number of tokens to generate in the response
max_tokens = 1024

# Generate a response
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

response = completion.choices[0].text
# Print the response
print(response)


bridge = get_bridge()

bridge.lights[0].hue = int(response)

# for light in bridge.lights:
#     print(light.name)
#     print(light.light_id)
