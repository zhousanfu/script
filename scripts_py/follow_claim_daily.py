# coding=utf-8
'''
Author: sanford courageux_san@wechat.com
Date: 2024-10-21 10:25:54
LastEditors: sanford courageux_san@wechat.com
LastEditTime: 2024-12-28 22:24:26
FilePath: /script/scripts_py/follow_claim_daily.py
Description: 
'''
import json
import time
import requests
import logging



logging.basicConfig(
    filename='log/follow_claim_daily.log',
    filemode="a+",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

with open('config/config.json', 'r') as f:
    config = json.load(f)

def claim_daily(csrf: str, cookie: str, **kwargs):
    url = 'https://api.follow.is/wallets/transactions/claim_daily'
    data = {
        "csrfToken": csrf,
    }
    headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/4G Language/zh_CN',
            'content-type': 'application/json',
            'Accept': '*/*',
            'cookie': cookie
        }
    reslut = requests.post(url, json=data, headers=headers)
    code = reslut.json()["code"]
    if code == 0 or code == 4000:
        logger.info(msg=f'claim_daily: {reslut.text}, user_name={kwargs['name']}')
    else:
        logger.error(msg=f'claim_daily: {reslut.text}, user_name={kwargs['name']}')

def transaction(csrf: str, cookie: str, **kwargs):
    url = 'https://api.follow.is/wallets/transactions/tip'
    data = {
        "entryId":"71443954160552960",
        "amount":"20000000000000000000",
        "csrfToken":csrf
        }
    headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/4G Language/zh_CN',
            'content-type': 'application/json',
            'Accept': '*/*',
            'cookie': cookie
        }
    reslut = requests.post(url, json=data, headers=headers)
    code = reslut.json()["code"]
    if code == 0 or code == 4000:
        logger.info(msg=f'transaction: {reslut.text}, user_name={kwargs['name']}')
    else:
        logger.error(msg=f'transaction: {reslut.text}, user_name={kwargs['name']}')



if __name__=="__main__":
    for i in config["FOLLOW_COOKES"]:
        claim_daily(csrf=i['csrf'], cookie=i['cookie'], name=i['name'])
    time.sleep(1)
    for i in config["FOLLOW_COOKES"]:
        if i['name'] != "sanford github 1" and i['name'] == "SanfordCi Goggle 2":
            transaction(csrf=i['csrf'], cookie=i['cookie'], name=i['name'])
