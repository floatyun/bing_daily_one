import os
import sys
import datetime
import time
import requests
from bs4 import BeautifulSoup
import prepare
import glob


def get_bg_img_link(url, host, link='https://cn.bing.com/'):
    # 获取bing首页
    headers = prepare.edge_headers(host)
    r = requests.get(url=url, timeout=2)
    print('页响应状态码：', r.status_code)

    # 利用BeautifulSoup解析bing首页获取背景图片地址的一部分
    # 以下主要是利用浏览器的审查元素
    # 所以要做修改的话，需要浏览器审查元素以做具体修改
    # 通过id定位
    soup = BeautifulSoup(r.text, "lxml")
    bg_img_link = soup.find("link", id="bgLink")['href']
    bg_img_link = bg_img_link[:bg_img_link.find('''&rf=''')]

    # 链接前半部分和后半部分拼接的细节处理
    # 避免两个斜杆('/')拼一起或者前后两部分都没有斜杆
    if link[-1] != '/':
        link += '/'
    if bg_img_link[0] == '/':
        bg_img_link = bg_img_link[1:]

    # 返回拼接好的完整的图片地址
    return link+bg_img_link


def get_img_and_save(img_link, host, prefix):
    filename = prefix + str(datetime.date.today())
    pos = len(filename)
    filename += img_link[img_link.rfind('.'):]
    print(filename)
    headers = prepare.download_img_headers(host)
    img = requests.get(url=img_link, headers=headers).content
    with open(filename, 'wb') as f:
        f.write(img)
    print(img_link)
    print('成功下载图片并保存为', filename)
    return True


def load_saved_links(today_log):
    saved_links = []
    try:
        f = open(today_log, "r")
        for line in f:
            saved_links.append(line.strip())
        f.close()
    except IOError:
        print('未检测到' + today_log)
        print('断定今日还未保存任何图片')
    return saved_links


def clear_logs_not_doday(today_log):
    log_files = glob.glob('*.log')
    for log in log_files:
        if log != today_log:
            os.remove(log)


def main():
    os.chdir(R'd:\bing_wallpapers')

    today = str(datetime.date.today())
    today_log = today + '.log'

    clear_logs_not_doday(today_log=today_log)
    saved_links = load_saved_links(today_log=today_log)  # 载入已经下载保存的图片地址
    down_links = []

    host = 'cn.bing.com'
    urls = [
        'https://cn.bing.com/?FORM=BEHPTB',
        'https://cn.bing.com/?FORM=BEHPTB&ensearch=1'
    ]

    for url in urls:
        img_link = get_bg_img_link(
            url=url, host=host)
        if (img_link not in saved_links) and (img_link not in down_links):
            down_links.append(img_link)

    new_saved_links = []
    off = len(saved_links)
    for index, img_link in enumerate(down_links):
        if get_img_and_save(img_link, host=host, prefix='%02d_' % (index + off)):
            new_saved_links.append(img_link)

    # 新下载保存的链接附加方式写入日志
    with open(today_log, 'a+') as f:
        for l in new_saved_links:
            f.writelines(l + '\n')

    print('运行完毕')


if __name__ == '__main__':
    main()
    os.system("pause")
