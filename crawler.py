from bs4 import BeautifulSoup
from collections import deque
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import re
import pymysql
import requests

#抓取freebuf链接
def get_freebufLink():
    global browser
    html = BeautifulSoup(browser.page_source, "lxml")
    href = html.find_all('a', class_='article-title')
    if href is not None:
        for each in href:
            link = each.get('href')
            if link not in visited:
                visited.add(link)
                queueFreebuf.append(link)
    div=html.find('div',class_='news-more')
    if div is not None:
        div_a = BeautifulSoup(str(div), "lxml")
        link = div_a.a
        if link is not None:
            link=link.get('href')
            visited.add(link)
            queueFreebuf.append(link)

#抓取github链接
def get_githubLink():
    global browser
    global count
    html = BeautifulSoup(browser.page_source, "lxml")
    regexp=re.compile("(https?)://github.com/[-A-Za-z0-9+&@#%?=~_|!:]+/[-A-Za-z0-9+&@#%=~_|]+")
    github_url=html.find_all(text=regexp)
    if github_url is None:
        return
    for each in github_url:
        url = re.search("(https?)://github.com/[-A-Za-z0-9+&@#%?=~_|!:]+/[-A-Za-z0-9+&@#%=~_|]+", each)
        url = url.group()
        url=url.strip()
        if url not in got:
            got.add(url)
            queueGithub.append(url)
            count=count+1
            print('GET  '+url)

#抓取github项目内容
def get_githubContent(content,url):
    global db
    cursor=db.cursor()
    description=content.find('span',class_='col-11 text-gray-dark mr-2')
    if description is not None:
        description=description.text.strip()
    title=content.find('h1',class_='public ')
    if title is not None:
        title=title.strong.a.text
        title=title.strip()
    else:
        return
    star = content.find('a', class_='social-count js-social-count')
    if star is not None:
        star=star.text.strip()
    sql="INSERT INTO project VALUES ('%s','%s','%s',%s)" % (title,description,url,star)
    try:
        cursor.execute(sql)
        db.commit()
        print('SAVE  '+title)
    except:
        db.rollback()

homepage='http://www.freebuf.com/sectool'
queueFreebuf=deque() #freebuf url队列
queueGithub=deque() #github url队列
visited=set() #访问过的freebuf 链接集合
got=set() #抓取过的github 链接集合
browser=webdriver.Firefox()
browser.set_page_load_timeout(10)
browser.set_script_timeout(10)
count=0
print("开始...")
db=pymysql.connect("localhost","root","","crawler") #链接数据库
cursor=db.cursor()
sql="""CREATE TABLE project(
       title VARCHAR(100) PRIMARY KEY,
       description VARCHAR(500),
       url VARCHAR(100),
       star SMALLINT)"""
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
browser.get(homepage)
wait = WebDriverWait(browser, 10)
element = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "article-title")))
visited.add(homepage)
get_freebufLink()
while queueFreebuf:
    url=queueFreebuf.popleft()
    try:
        browser.get(url)
    except:
        browser.execute_script('window.stop()')
    if 'page' in url:
        try :
            wait = WebDriverWait(browser, 10)
            element = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "article-title")))
        except:
            queueFreebuf.append(url)
            continue
        get_freebufLink()
    else:
        #element = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "articlecontent")))
        get_githubLink()
print('-------------------------------------------')
print('共找到 ', count, ' 个Github项目')
print('\n开始抓取Github项目...')
while queueGithub:
    url=queueGithub.popleft()
    try:
        req=requests.get(url,timeout=10)
    except:
        queueGithub.append(url)
        continue
    try:
        content=BeautifulSoup(req.text,"lxml")
    except:
        continue
    get_githubContent(content,url)
print('-------------------------------------------')
print('结束')
db.close() # 关闭数据库连接