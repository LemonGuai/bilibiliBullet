import requests
import re
import MySqlHelper
import datetime

headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

proxies = {
    'http': 'http://49.77.209.240:9999'
    # 'http': 'http://114.224.114.203:9999'
    # 'http': 'http://114.239.150.191:9999'
    # 'http': 'http://185.101.236.76:63141'
    # 'http': 'http://223.242.247.244:9999'
    # 'http': 'http://183.166.162.220:9999'
}


def __GetHtml__(Page):
    url = 'https://www.kuaidaili.com/free/inha/{0}'
    try:
        url = url.format(Page)
        html_text = requests.get(url, headers, proxies=proxies).text
    except Exception as error:
        print("获取代理IP网页信息出错,网页url:【{0}】,错误信息:【{1}】".format(url, error))
    # 返回页面内容
    return html_text


def __GetIPList__(Html):
    GetIPList_re = re.compile(r'(<td data-title="IP">.*?"最后验证时间".*?</td>)', re.S)
    # IPList = re.findall(GetIPList_re,Html)
    IPList = GetIPList_re.findall(Html)
    return IPList


def __GetIPInfo__(IPList):
    # <td data-title="IP">(.*)<.*data-title="PORT">(.*)<.*data-title="匿名度">(.*)<.*data-title="类型">(.*)<.*data-title="位置">(.*)<.*data-title="响应速度">(.*)<.*data-title="最后验证时间">(.*)</td>
    # GetIP_re = re.compile(r'<td data-title="IP">(.*)<.*\s.*"PORT">(.*)<.*\s.*"匿名度">(.*)<.*\s.*"类型">(.*)<.*\s.*"位置">(.*)<.*\s.*"响应速度">(.*)<.*\s.*"最后验证时间">(.*)</td>')
    GetIP_re = re.compile(r'<td data-title="IP">(.*)</.*"PORT">(.*)</.*"匿名度">(.*)</.*"类型">(.*)</.*"位置">(.*)</.*"响应速度">(.*)</.*"最后验证时间">(.*)</td>', re.S)
    oResultList = list()
    for item in IPList:
        oList = list()
        oList.append(GetIP_re.search(item).group(1))  # IP
        oList.append(GetIP_re.search(item).group(2))  # Port
        oList.append(GetIP_re.search(item).group(4))  # 类型
        oList.append(GetIP_re.search(item).group(3))  # 匿名度
        iResponse = GetIP_re.search(item).group(6).replace('秒', '')
        oList.append(iResponse)  # 响应速度
        # 有效性默认0
        # 使用次数默认0
        oList.append(GetIP_re.search(item).group(5))  # 位置
        oList.append(GetIP_re.search(item).group(7))  # 验证日期
        # 获取操作日期
        optiondate = datetime.datetime.now()
        optiondate = datetime.datetime.strftime(optiondate, '%Y-%m-%d %H:%M:%S')
        oList.append(optiondate)  # 操作日期
        oParamTuple = tuple(oList)
        oResultList.append(oParamTuple)
    oResultTuple = tuple(oResultList)
    return oResultTuple


def __AgentIPIsValid__(type, IP, Port):
    result = 0
    url = 'http://icanhazip.com'
    proxy = {type: IP+':'+Port}
    IPResult = requests.get(url, proxies=proxy).text
    if IP == IPResult:
        result = 1
    return result


def main():
    print('请输入想要爬取页数:')  # 修改 可输入bv号,视频链接,视频名称
    sPage = int(input())
    html_text = __GetHtml__(sPage)
    IPList = __GetIPList__(html_text)
    oResultTuple = tuple()
    oResultTuple = __GetIPInfo__(IPList)
    mysql = MySqlHelper.DBHelper(flag=1)
    # for iTuple in oResultTuple:
    count = mysql.ExecuteNonQryText("free_agent_IP_ins.sql", oResultTuple)
    print('爬取结果:')
    print("共{0}条".format(count))


if __name__ == '__main__':
    main()
