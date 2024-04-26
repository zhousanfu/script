#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-25 20:24:29
 LastEditors: Sanfor Chow
 LastEditTime: 2024-04-25 20:24:30
 FilePath: /script/当当网评论.py
'''
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup, element

# productId: 商品的id
# pageIndex: 评论分页 只能获取前200页
# sortType: 精彩评论1 时间排序2
# filterType: 全部1 好评2 中评3 差评4 晒图5
# tagId和tagFilterCount: 关键词过滤，这里用不着就不分析了



def parse_item(item: element.Tag):
    image_links = []

    star_box = item.find('span', class_='star_box')
    star_percentage = star_box.find('span', class_='star')['style']
    star_percentage = star_percentage.split(':')[1].strip()
    rating = item.find('em').text
    comment_text = item.find('div', class_='describe_detail').text.strip()
    pic_show = item.find('ul', class_='pic_show')
    if pic_show is not None:
        li_items = pic_show.find_all('li')
        for li in li_items:
            img = li.find('img')
            if img is not None and 'data-big-pic' in img.attrs:
                image_links.append(img['data-big-pic'])
    starline = item.find('div', class_='starline')
    timestamp = starline.find('span').text
    version = starline.find_all('span')[1].text
    support = item.find('div', class_='support')
    like_count = support.find('a', class_='j_zan')['data-number']
    reply_count = support.find('a', class_='reply_new')['data-number']

    data = {
        '评论星级': star_percentage,
        '评论评分': rating,
        '评论内容': comment_text,
        '评论的所有图片': image_links,
        '发表时间': timestamp,
        '版本信息': version,
        '评论点赞数': like_count,
        '回复数': reply_count
    }
    return data

def parse_page(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find(attrs={'class': 'fanye_box'}) is None:
        return None
    cmt_list = soup.find_all(attrs={'class': 'comment_items clearfix'})
    return cmt_list

def get_parse(product_id):
    # productId: 商品的id
    # pageIndex: 评论分页 只能获取前200页
    # sortType: 精彩评论1 时间排序2
    # filterType: 全部1 好评2 中评3 差评4 晒图5
    # tagId和tagFilterCount: 关键词过滤，这里用不着就不分析了
    comments = []
    url = 'http://product.dangdang.com/index.php'
    params = {
        'r': 'comment/list',
        'productId': product_id,
        'categoryPath': '01.41.26.19.00.00',
        'mainProductId': product_id,
        'mediumId': '0',
        'pageIndex': '1',
        'sortType': '1',
        'filterType': '1',
        'isSystem': '1',
        'tagId': '0',
        'tagFilterCount': '0',
        'template': 'publish'
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'http://product.dangdang.com/29414183.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
        'X-Requested-With': 'XMLHttpRequest'
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        html = data['data']['list']['html']
        item_wraps = parse_page(html=html)
        for ite in item_wraps:
            comments.append(parse_item(ite))
    else:
        print('请求失败')

    return comments




column_names = ['评论星级','评论评分','评论内容','评论的所有图片','发表时间','版本信息','评论点赞数','回复数']
df = pd.DataFrame({}, columns=column_names)
df.to_csv('当当网评论.csv', sep=',', header=True, index=False)

comments = get_parse(product_id='29414183')

new_df = pd.DataFrame(comments, columns=column_names)
new_df.to_csv('当当网评论.csv', sep=',', header=False, index=False, mode='a')