import requests
import re
import os
from lxml import etree

headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

proxies = {
    'http': 'http://49.77.209.240:9999',
    'http': 'http://114.224.114.203:9999',
    'http': 'http://114.239.150.191:9999',
    'http': 'http://185.101.236.76:63141',
    'http': 'http://223.242.247.244:9999',
    'http': 'http://183.166.162.220:9999',
}

BV = ""


def __GetHtml(SearchStatement):
    url = ""
    html_text = ""
    global BV

    if len(SearchStatement) == 0:
        return "请输入BV号,视频链接或视频名称"
    BVPattern = r'BV\w{10}'
    UrlPattern = r'https://www\.bilibili\.com\/video\/BV(\w{10})\?spm_id_from=(.*)'

    if re.match(BVPattern, SearchStatement):  # 匹配bv号
        url = "https://www.bilibili.com/video/{0}".format(SearchStatement)
        BV = SearchStatement
    elif re.match(UrlPattern, SearchStatement):  # 匹配视频链接
        url = SearchStatement
        BV = re.match(UrlPattern, SearchStatement).group(1)
    else:  # 视频名称
        SearchUrl = "https://search.bilibili.com/all?keyword={0}".format(
            SearchStatement)
        __GetSearchResult(SearchUrl)
    # 获取请求的url页面内容
    try:
        if len(url) > 0:
            html_text = requests.get(url, headers, proxies=proxies).text
    except Exception as error:
        print("获取视频网页信息出错,BV号:{0},错误信息:{1}".format(BV, error))
    # 返回页面内容
    return html_text


def __GetSearchResult(SearchUrl):
    searchHTML = requests.get(SearchUrl, headers).text
    pattern = r''


# 获取弹幕列表
def __GetBulletList(html_text, BV):
    pattern = 'cid=(\d+)&aid=(\d+)&attribute'
    cid = re.search(pattern, html_text).group(1)  # 获取cid
    url = "https://api.bilibili.com/x/v1/dm/list.so?oid={0}".format(cid)
    try:
        bullet_text = requests.get(url, headers, roxies=proxies).content  # 获取弹幕内容
    except Exception as error:
        print("获取视频弹幕列表出错,BV号:{0},错误信息:{1}".format(BV, error))
    return bullet_text


def __HandleBulletText(bullet_text, SearchStatement):
    xml = etree.fromstring(bullet_text)
    bullet_list = xml.xpath('//i//d//text()')
    BV = ""
    BVPattern = r'BV\w{10}'
    UrlPattern = r'https://www\.bilibili\.com\/video\/BV(\w{10})\?spm_id_from=(.*)'
    if re.match(BVPattern, SearchStatement):  # 匹配bv号
        BV = 'BV' + SearchStatement
    elif re.match(UrlPattern, SearchStatement):  # 匹配视频链接
        BV = re.match(UrlPattern, SearchStatement).group(1)
    filename = 'bilibili_bullet_list_{0}.txt'.format(BV)
    path = 'programs/爬虫/b站弹幕/{0}'.format(filename)
    # path = os.getcwd()+format(filename)
    with open(path, 'w', encoding='utf-8') as myfile:
        for i in bullet_list:
            myfile.write(i + '\n')
    return path


def main():
    print('请输入想要爬取弹幕的视频BV号或链接:')  # 修改 可输入bv号,视频链接,视频名称
    SearchStatement = input()
    html_text = __GetHtml(SearchStatement)
    bullet_text = __GetBulletList(html_text, BV)
    path = __HandleBulletText(bullet_text, SearchStatement)
    print("爬取的弹幕保存路径为:{0}".format(path))


if __name__ == '__main__':
    main()