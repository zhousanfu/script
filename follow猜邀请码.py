# coding=utf-8
'''
 Author: courageux_san WX
 Date: 2024-10-10 20:09:39
 LastEditors: courageux_san WX
 LastEditTime: 2024-10-19 20:28:05
 FilePath: /script/follow猜邀请码.py
 猜邀请码 把*替换成可能的字符,生成所有可能
'''
import os
import requests
import itertools
import string
import time



CSRFTOKEN = os.getenv("CSRFTOKEN")
COOKIE = os.getenv("COOKIE")

code = 'rqlKkl*0f9'

code_list = []
# characters = string.digits                # 0~9
characters = string.ascii_letters        # a~z A~Z
asterisk_positions = [i for i, char in enumerate(code) if char == '*']
for combination in itertools.product(characters, repeat=len(asterisk_positions)):
    new_code = list(code)       # 将字符串转换为列表以便修改
    for pos, char in zip(asterisk_positions, combination):
        new_code[pos] = char    # 替换 '*'
        if "*" not in ''.join(new_code):
            code_list.append(''.join(new_code))
print('所有组合的数量:', len(code_list))

for c in code_list:
    data = {
        "code": c,
        "csrfToken": CSRFTOKEN
    }
    headers = {
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Origin": "https://app.follow.is",
        "Alt-Svc": 'h3=":443"; ma=86400',
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": COOKIE,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "X-App-Dev": "0",
        "X-App-Version": "0.0.1-alpha.19",
    }
    r = requests.post(url='https://api.follow.is/invitations/use', json=data, headers=headers)
    print(c, '返回:', r.json())
    time.sleep(0.01)