# coding=utf-8
'''
Author: sanford courageux_san@wechat.com
Date: 2024-12-28 09:38:55
LastEditors: sanford courageux_san@wechat.com
LastEditTime: 2024-12-30 16:51:56
FilePath: /script/ai_api/xai.py
Description: 
'''
import os
import asyncio
from openai import OpenAI



XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(
        api_key=XAI_API_KEY,
        base_url="https://api.x.ai/v1",
    )


async def chat(prompt, model_name="grok-2-latest", structur:bool = True, Response=None):
    results = None

    if structur:
        completion = client.beta.chat.completions.parse(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format=Response,
        )
        results = completion.choices[0].message.content
    else:
        stream = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            if chunk:
                res = chunk.choices[0].delta.content
                if res:
                    results += res

    return results

def img(url):
    image_url = (
        "https://science.nasa.gov/wp-content/uploads/2023/09/web-first-images-release.png"
    )

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                        "detail": "high",
                    },
                },
                {
                    "type": "text",
                    "text": "What's in this image?",
                },
            ],
        },
    ]

    completion = client.chat.completions.create(
        model="grok-2-vision-1212",
        messages=messages,
        temperature=0.01,
    )

    print(completion.choices[0].message.content)



if __name__ == "__main__":
    res = asyncio.run(chat(prompt="你是谁"))
    print(res)