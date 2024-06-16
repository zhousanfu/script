#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-05-03 06:55:45
 LastEditors: courageux_san WX
 LastEditTime: 2024-06-14 12:15:52
 FilePath: /script/api/llm_groq.py
'''
import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def llm_groq(text):
    messages = [{
        'role': 'system',
        'content': text
        }]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="Llama3-70b-8192",
    )
    # print(chat_completion.choices[0].message.content)

    return chat_completion.choices[0].message.content



if __name__=="__main__":
    llm_groq(text="蒙古文本纠错:тэндээс могнголын цэргийн байдлыг ахиглан харвал голын хөвөө агаж гал галаар ялгаран буужээ .")