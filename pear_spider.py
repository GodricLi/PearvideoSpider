# _*_coding:utf-8 _*_
# @Author　 : Ric
"""使用多线程爬取梨视频视频数据"""
import requests
import re
from lxml import etree
from multiprocessing.dummy import Pool

url = 'https://www.pearvideo.com/category_5'
page_text = requests.get(url=url).text

tree = etree.HTML(page_text)
li_list = tree.xpath('//ul[@id="listvideoListUl"]/li')
url_list = []
for i in li_list:
    detail_url = "https://www.pearvideo.com/" + i.xpath('./div/a/@href')[0]
    name = i.xpath('./div/a/div[2]/text()')[0] + '.mp4'
    detail_page = requests.get(url=detail_url).text
    ex = 'srcUrl="(.*?)",vdoUrl'
    video_url = re.findall(ex, detail_page)[0]
    dic = {
        'name': name,
        'url': video_url
    }
    url_list.append(dic)


def get_video_data(d):
    url = d['url']
    data = requests.get(url=url).content
    print(d['name'], "正在下载。。。")
    with open(d['name'], 'wb') as f:
        f.write(data)
        print(d['name'], "下载成功。。。")


pool = Pool(4)
pool.map(get_video_data, url_list)
pool.close()
pool.join()
