### 胡说八道的背景交代
一直对bing 的主页的图片流口水，然而，貌似那个不是挺好保存的，虽然可以通过审查元素，然后ctrl+f获取地址，然后保存，但是操作实在是繁琐。  
前几个月的时候也曾网上百度过bing每日一图的爬虫代码。然而，真正的搜索结果感觉就2-3个。  
比较不幸的是有着“只获取了国内版的”、“使用的python版本比较老以致我无法解决第三方依赖库”、“莫名的问题”等等之类的问题，里面有一个能爬取国内版的比较靠谱的，然后就算很开心了，但是那个貌似使用的是据说微博里bing给的一个什么图片地址的，然后只有国内版，所以尝试着改成国际版失败了。  
**于是那个时候立了个flag——有空的时候自己写一下爬虫去爬取。**  
忙了几个月学业之后，暑假总算有点自由的时间了。于是学了一下爬虫，迫不及待的就开始用爬虫来爬取bing首页图片了。  
### 时间及相关软件版本备注
**测试时间2019年7月15日**
| 条目           |   版本 |
| :------------- | -----: |
| Python         |  3.7.2 |
| bs4            |  0.0.1 |
| beautifulsoup4 |  4.7.1 |
| requests       | 2.22.0 |
| lxml           |  4.3.4 |
### 代码
* `prepare.py`
```python
def edge_headers(host):
    headers = {
        'Host': host,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
    }
    return headers


def download_img_headers(host):
    headers = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3',
        'Host': host,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
    }

```
* `get_background.py`
```python
import os
import sys
import datetime
import requests
from bs4 import BeautifulSoup
import prepare


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
    filename = prefix + str(datetime.date.today()) + img_link[img_link.rfind('.'):]
    filename = '''d:\bing_wallpaper''' + '\\' + filename
    headers = prepare.download_img_headers(host)
    img = requests.get(url=img_link, headers=headers).content
    with open(filename, 'wb') as f:
        f.write(img)
    print(img_link)
    print('成功下载图片并保存为', filename)


def main():
    host = 'cn.bing.com'
    img_link = get_bg_img_link(url = 'https://cn.bing.com/?FORM=BEHPTB', host=host)
    get_img_and_save(img_link, host=host, prefix='国内版')
    
    img_link = get_bg_img_link(url = 'https://cn.bing.com/?FORM=BEHPTB&ensearch=1', host=host)
    get_img_and_save(img_link, host = host, prefix='国际版')
    print('运行完毕')



if __name__ == '__main__':
    main()

```

### 测试说明
目前仅仅测试过一次，成功的把国内版和国际版各一张爬下来了。  
However, 大概就在15点30分。我再运行一次的时候，惊奇地发现居然国内版和国际版得到地是同一张图片，不知原因。  
后来发现浏览器打开看到的也是同一张图片。另外我发现貌似bing现在首页不只一张图片了，右下角是有下一张可供切换的，以及有些图片是有下载按钮供直接下载当壁纸。这么看来bing已经很为用户着想了，不能下载的应该是版权方面的问题。  
不过话说我这个程序发现发现问题也太快了。让我哭一会儿。 

