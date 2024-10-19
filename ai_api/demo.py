#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-25 20:19:58
 LastEditors: courageux_san WX
 LastEditTime: 2024-10-19 20:43:00
 FilePath: /script/ai_api/demo.py
'''
from tqdm import tqdm
from llm_groq import llm_groq



data = open('demo.txt', 'r', encoding='utf-8').readlines()
data = [i.strip() for i in data]

out = []
for i, item in enumerate(tqdm(range(len(data)), desc="Processing data"), 1):
    if i % 50 == 0:
        prompt = '操作下方文本: \n{}'.format("\n".join(data[i-50 : i]))
        r = llm_groq(text=prompt)
        for x in r.split('\n')[2:]:
            out.append(x)

with open('tmp.txt', 'w', encoding='utf-8') as file:
    for o in out:
        file.write(o + '\n')
file.close()