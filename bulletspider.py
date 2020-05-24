import requests
import re
import os
from lxml import etree


def main():
    print('请输入想要爬取弹幕的视频BV号:')
    BV = input()
    html_text = __GetHtml(BV)
    bullet_text = __GetBulletList(html_text)
    path = __HandleBulletText(bullet_text, BV)
    print("爬取的弹幕保存路径为:{0}".format(path))


if __name__ == '__main__':
    main()


headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}


def __GetHtml(BV):
    # 拼视频的url
    url = "https://www.bilibili.com/video/{0}".format(BV)
    # 获取请求的url页面内容
    html_text = requests.get(url, headers).text
    # 返回页面内容
    return html_text


def __GetBulletList(html_text):

    pattern = 'cid=(\d+)&aid=(\d+)&attribute'
    cid = re.search(pattern, html_text).group(1)
    url = "https://api.bilibili.com/x/v1/dm/list.so?oid={0}".format(cid)
    bullet_text = requests.get(url, headers).content
    return bullet_text


def __HandleBulletText(bullet_text, BV):
    xml = etree.fromstring(bullet_text)
    bullet_list = xml.xpath('//i//d//text()')
    filename = 'bilibili_bullet_list_{0}.txt'.format(BV)
    path = 'programs/爬虫/b站弹幕/{0}'.format(filename)
    # path = os.getcwd()+format(filename)
    with open(path, 'w', encoding='utf-8') as myfile:
        for i in bullet_list:
            myfile.write(i + '\n')
    return path

