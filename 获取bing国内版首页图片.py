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


def get_img_and_save(img_link, host, prefix, force_download=False):
    filename = prefix + str(datetime.date.today())
    pos = len(filename)
    filename += img_link[img_link.rfind('.'):]
    print(filename)
    if os.path.exists(filename):
        if not force_download:
            print(filename, "已经存在了，故不下载。若想强制下载请添加添加一个-f参数")
            return
        else:
            print(filename, "已经存在了，因强制下载需求，故增添时间标识")
            filename = filename[:pos] + \
                time.strftime("_%H_%M_%S", time.localtime()) + filename[pos:]

    headers = prepare.download_img_headers(host)
    img = requests.get(url=img_link, headers=headers).content
    with open(filename, 'wb') as f:
        f.write(img)
    print(img_link)
    print('成功下载图片并保存为', filename)


def main(force_download=False):
    os.chdir(R'd:\bing_wallpapers')
    host = 'cn.bing.com'
    img_link = get_bg_img_link(
        url='https://cn.bing.com/?FORM=BEHPTB', host=host)
    get_img_and_save(img_link, host=host, prefix='国内版',
                     force_download=force_download)

    img_link = get_bg_img_link(
        url='https://cn.bing.com/?FORM=BEHPTB&ensearch=1', host=host)
    get_img_and_save(img_link, host=host, prefix='国际版',
                     force_download=force_download)
    print('运行完毕')


if __name__ == '__main__':
    force_download = '-f' in sys.argv or '-F' in sys.argv
    main(force_download=force_download)
    os.system("pause")
