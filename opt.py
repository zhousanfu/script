#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-25 20:19:58
 LastEditors: Sanfor Chow
 LastEditTime: 2024-04-25 20:19:59
 FilePath: /script/opt.py
'''
import re
import time
from tqdm import tqdm
import pandas as pd
from my_lls import rewrite_text_with_genai



def opt(data):
    out_data = []
    pbar = tqdm(total=len(data))
    for i in data:
        if isinstance(i[1], str):
            # prompt = f'将“{i[1]}”里面的语气词改成“{i[0].split("——")[1]}”'
            prompt = f'使用“{i[0].split("——")[1]}”这个语气助语编写五条关于“{i[2].split(".")[1]}”语境意思的句子, 要求五条句子不能重复相类'
            res = rewrite_text_with_genai(text='', prompt=prompt)
            # out_data.append(res)
            out_data.append(i[2].strip() + "\t" + "\t".join(re.split(r'\d+\.+', res.replace('\n', ''), flags=re.MULTILINE)[1:]))
            time.sleep(1)
        pbar.update(1)
    pbar.close()

    return out_data

df = pd.read_excel('Appen014语料模板.xlsx', sheet_name='Sheet1')
df['语气词'] = df['语气词'].fillna(method='ffill')
out_data = opt(data=df[['语气词', '语料', '语气特征（细分编号）']].values)

with open('tmp_B.txt', 'w') as file:
    for fruit in out_data:
        file.write(fruit + '\n')
file.close()