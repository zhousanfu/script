#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-25 20:19:58
 LastEditors: courageux_san WX
 LastEditTime: 2024-06-14 12:31:41
 FilePath: /script/opt.py
'''
import re
import time
from tqdm import tqdm
import pandas as pd
from api.llm_groq import llm_groq




# df = pd.read_excel('Appen014语料模板.xlsx', sheet_name='Sheet1')
# df['语气词'] = df['语气词'].fillna(method='ffill')
# out_data = opt(data=df[['语气词', '语料', '语气特征（细分编号）']].values)

data = open('test_spell_error_5月1日后发布.txt', 'r', encoding='utf-8').readlines()
data = [i.strip() for i in data]

# out = []
# for i in tqdm(data, desc="Processing data"):
#     prompt = f'蒙古文本纠错,只返回修正后的文本, 保留原先的符号:\n{i}'
#     r = llm_groq(text=prompt)
#     # print(r)
#     # for i in r.split("\n"):
#     #     if '"' in i:
#     #         print(i)
#     out.append(r)
#     # break

out = []
for i, item in enumerate(tqdm(range(len(data)), desc="Processing data"), 1):
    if i % 50 == 0:
        prompt = '蒙古文本纠错,只返回修正后的文本,返回结果一行对应一行,保留原先的符号:\n{}'.format("\n".join(data[i-50 : i]))
        r = llm_groq(text=prompt)
        for x in r.split('\n')[2:]:
            out.append(x)

with open('tmp.txt', 'w', encoding='utf-8') as file:
    for o in out:
        file.write(o + '\n')
file.close()