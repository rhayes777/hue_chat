import json
import os
from json import JSONDecodeError
from typing import List

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


class ChatBot:
    def __init__(
            self,
            engine="gpt-3.5-turbo",
            max_tokens=1024,
            temperature=0.1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            header="",
    ):
        """
        Keep track of messages submitted by the user and generate responses
        by calling the OpenAI API.

        Parameters
        ----------
        engine
        max_tokens
        temperature
        top_p
        frequency_penalty
        presence_penalty
            OpenAI configuration parameters
        header
            The header to prepend to the user's messages
        """
        self.engine = engine
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

        self.header = header

    def __call__(self, message: str) -> List[dict]:
        """
        Submit the header and all previous messages to the chat bot and return the response.

        Parameters
        ----------
        message
            A new message added by the user

        Returns
        -------
        The response from OpenAI as a list of dictionaries containing the color and light_id
        for each light.
        """
        prompt = f"{self.header}\n{message}"
        text = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
        ).choices[0].text.strip(" .\t\n")
        try:
            return json.loads(text)
        except JSONDecodeError:
            print(text)
            raise
