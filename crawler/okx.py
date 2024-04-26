#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-25 20:23:57
 LastEditors: Sanfor Chow
 LastEditTime: 2024-04-25 20:23:58
 FilePath: /script/okx.py
'''
import requests
import datetime



current_datetime = datetime.datetime.now()
current_timestamp = int(current_datetime.timestamp() * 1000)  # 获取当前时间戳（毫秒）
print("当前时间戳（毫秒级）:", current_timestamp)

timestamp = current_timestamp / 1000  # 将时间戳转换为秒（除以1000）
dt_object = datetime.datetime.fromtimestamp(timestamp)
print("转换后的日期时间:", dt_object)

host = input("请输入主机名（默认为www.okx.com）：") or "www.okx.com"
print("主机名：", host)


url = f"https://{host}/priapi/v5/market/candles?instId=BTC-USDT&before=1683276765000&bar=1Dutc&limit=329&t={current_timestamp}"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Connection": "keep-alive",
    "Host": "www.okx.com",
    "Referer": "https://www.okx.com/zh-hans/trade-spot/btc-usdt",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15"
}

response = requests.get(url, headers=headers)

print("状态码:", response.status_code)
print("响应内容:", response.text)