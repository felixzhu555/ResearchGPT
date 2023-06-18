import requests
import json
import os

API_KEY = "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"
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"


def query_gpt(messages, model="gpt-4", temperature=1, max_tokens=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant with culinary expertise.",
    },
    {
        "role": "user",
        "content": "I have tomatoes, chicken breast, cauliflower, and red wine. What recipes are there that utilize these ingredients?",
    },
]
