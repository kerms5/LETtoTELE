import cloudscraper
import feedparser
import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# 全局参量
# rss源链接
feeds = []
entries = []
# 机器人参数合辑
baseuri = 'https://api.telegram.org/bot'
method = '/sendMessage?chat_id='
chat_id = ""  # Userid
token = ""  # 机器人 TOKEN

# 获取全部rss源链接
def getfeeds():
    rawdata = scraper.get("https://lowendtalk.com/categories").text
    soup = BeautifulSoup(rawdata,'lxml')
    # 获取所有a、并且属性符合的元素
    link = soup.select('a[title="RSS Feed"]')
    for i in link:
        feeds.append('https://lowendtalk.com/'+i['href'])

# 监控函数
def monitor():
    # 获取所有rss链接内数据，并进行简单的数据美化处理
    for feed in feeds:
        rawdata = scraper.get(feed).text
        for entry in feedparser.parse(rawdata)['entries']:
            # 用beautifulsoup处理内容预览字段（原文为html格式），这里只截取第一段。
            # entry['summary'] = (BeautifulSoup(entry['summary'],'lxml').p).contents[0]
            # 查看是否存在此条记录
            cur.execute("""SELECT id FROM rss WHERE id=?""",(entry['id'],))
            result = cur.fetchone()
            if result:
                # 如果存在本记录，则无需进行发送
                pass
            else:
                # 调用信息发送
                # send(entry)
                # 将记录储存到数据库中
                cur.execute('''INSERT INTO rss values (?,?,?,?)''', (entry["id"],entry["title"],entry["published"],entry["link"]))
                conn.commit()
                print(entry)

def send(entry):
    # 不推送内容预览（可以通过tele自带的预览）
    massage = 'lowendtalk新帖推送\n'+'标题：'+entry['title']+'\n'+'发布时间：'+entry['published']+'\n'+'直达链接：'+entry['link']
    uri = baseuri+token+method+chat_id+'&text='+massage+'&parse_mode=html'
    requests.get(uri)
    # 每次发送信息间隔1s，防止信息阻塞
    time.sleep(1)

#############
# 函数主体
#############

# 初始化scraper
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

# 初始化sqlite
conn = sqlite3.connect('entries.db')
cur = conn.cursor()
# 首先尝试新建一个表
try:
    cur.execute('''CREATE TABLE rss (id text, title text, time text, link text)''')
except:
    pass
# 获取所有rss链接
getfeeds()
# 监控，每四分钟进行一次刷新
while True:
    monitor()
    time.sleep(4*60)

conn.close()