#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-05-03 06:55:45
LastEditors: sanford courageux_san@wechat.com
LastEditTime: 2024-12-28 09:34:12
FilePath: /script/ai_api/groq.py
'''
import os
from openai import OpenAI

XAI_API_KEY = os.getenv("GROQ_API_KEY")
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

stream = client.chat.completions.create(
    model="grok-2-latest",
    messages=[
        {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
        {"role": "user", "content": "What is the meaning of life, the universe, and everything?"},
    ],
    stream=True  # Set streaming here
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="", flush=True)


if __name__=="__main__":
    llm_groq(text="你是谁")