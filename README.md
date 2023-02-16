# Control Hue with ChatGPT

Small project illustrating how ChatGPT can be used to control Hue lights.

## Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up OpenAI API key

Get an API Key from [OpenAI](https://openai.com/api/).

Export it as an environment variable:

```bash
export OPENAI_API_KEY={your_api_key}
```

### Hue

You should be connected to the same WiFi network as your Hue bridge. 
When you first run the script you will need to press the button on 
the bridge to authorize the script.

## Run

Simply run the script:

```bash
./main.py
```

Enter commands like "turn on the lights", "turn off the lights" or "make one light blue and the other red"