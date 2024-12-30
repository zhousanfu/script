# coding=utf-8
'''
 Author: courageux_san WX
 Date: 2024-10-18 00:10:31
LastEditors: sanford courageux_san@wechat.com
LastEditTime: 2024-10-21 11:35:54
FilePath: /script/scripts_py/follow邀请码监听.py
'''
import os
import re
import time
import requests
import base64
import logging
from pathlib import Path
from PIL import Image
from io import BytesIO
from rapidocr_onnxruntime import RapidOCR



FOLLOW_CSRFTOKEN = os.getenv("FOLLOW_CSRFTOKEN")
FOLLOW_COOKE = os.getenv("FOLLOW_COOKE")
DISCORD_COOKIE = os.getenv("DISCORD_COOKIE")
DISCORD_AUTHORIZATION = os.getenv("DISCORD_AUTHORIZATION")

class UniqueList:
    def __init__(self, items):
        self.items = items  # 原始列表
        self.used_items = set()  # 用于跟踪已使用的元素

    def get_next(self):
        not_items = []
        for item in self.items:
            if item not in self.used_items:
                self.used_items.add(item)  # 标记为已使用
                not_items.append(item)
                
        return not_items

    def add_item(self, item):
        if item not in self.items and item not in self.used_items:
            self.items.append(item)  # 仅在未存在于列表和已使用集合中时添加
        # else:
        #     print(f"元素 {item} 已存在或已被使用，无法添加。")

def decode_base64(encoded_text="SFM1RXA3VkdzYQ=="):
    try:
        decoded_text = base64.b64decode(encoded_text).decode("utf-8")
    except ValueError:
        return ""
    return decoded_text

def regex_extract(text):
    extracts = []
    pattern_1 = r"[A-Za-z0-9_]{10}"
    pattern_2 = r"[A-Za-z0-9+]{10,}([^=]+={1,2})"

    extracts.extend([decode_base64(i) for i in re.findall(pattern_2, text)])
    extracts.extend(re.findall(pattern_1, text))
        
    return extracts

def image_to_text(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    # img_path = Path('image.png')

    engine = RapidOCR(text_score=0.6, det_use_cuda=False)
    result, elapse = engine(image)
    logger.info(f'image_to_text : {elapse}')
    
    return [i[1] for i in result]

def validation_follow(codes):
    r = None
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": FOLLOW_COOKE,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    for code in codes:
        if code != None and len(code) == 10:
            data = {"code": code, "csrfToken": FOLLOW_COOKE}
            r = requests.post(url='https://api.follow.is/invitations/use', json=data, headers=headers)
            logger.info(f'validation_follow code:{code}, 返回:{r.json()}')

def get_discord_contents(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Authorization': DISCORD_AUTHORIZATION,
        'Cookie': DISCORD_COOKIE,
        'Priority': 'u=3, i',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Discord-Locale': 'zh-CN',
        'X-Discord-Timezone': 'Asia/Shanghai',
    }
    r = requests.get(url=url, headers=headers)
    return r

codes = UniqueList([])
images = UniqueList([])
logging.basicConfig(
    filename='log/follow.log',
    filemode="w",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

while True:
    try:
        r1 = get_discord_contents(url='https://discord.com/api/v9/channels/1265925366820765818/messages?limit=10')
        time.sleep(0.05)
        r2 = get_discord_contents(url='https://discord.com/api/v9/channels/1265932718084984963/messages?limit=10')

        result = r1.json() + r2.json()
        print(f'\r最新一条消息:{result[0]['content'].replace('\n', ' ')}', end='')
        for i in result:
            contents = i['content'] + '\n'

            if len(i['attachments']) >= 1:
                for p in i['attachments']:
                    images.add_item(p['url'])
            
            image_urls = images.get_next()
            for url in image_urls:
                ima_text = image_to_text(image_url=url)
                contents += "\n".join(ima_text)

            code = regex_extract(contents)
            for c in code:
                codes.add_item(c)

        not_item = codes.get_next()
        # print(f'\rnot_item:{not_item}', end='')
        validation_follow(codes=not_item)
    except Exception as e:
        logging.error("发生了一个错误: %s", e)
        time.sleep(1)
    
    time.sleep(0.05)