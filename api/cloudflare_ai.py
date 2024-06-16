#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-26 21:38:33
 LastEditors: Sanfor Chow
 LastEditTime: 2024-04-26 22:13:06
 FilePath: /script/tmp.py
'''
import os
import requests

API_TOKEN = os.getenv('CF_API_TOKEN')
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/4b1656c6c88f9a0bbb4cd80491d58a30/ai/run/"


def text_to_image_dreamshaper(model, prompt, file_path):
    inputs = {
        "prompt": "prompt"
    }
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=inputs)
    
    if response.status_code == 200:
        with open('image.jpg', 'wb') as f:
            f.write(response.content)
    else:
        print('请求失败:', response.json())



if __name__=="__main__":
    text_to_image_dreamshaper("@cf/lykon/dreamshaper-8-lcm", prompt="cyberpunk cat", file_path='image.jpg')
