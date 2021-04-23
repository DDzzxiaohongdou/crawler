#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: DDZZxiaohongdou 2020/4/6 completed
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import numpy as np
from pandas import Series
from tqdm import tqdm
from selenium import webdriver #引入该模块解决网页动态加载问题
#解决每加载一次弹出浏览器的问题
from selenium.webdriver.chrome.options import Options
from PIL import Image,ImageEnhance
from matplotlib.pylab import mpl
#from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#城市与网页url的映射字典
#回头这一块可以优化下，改成通用化的。
house_dict = {'浦东':'pudong'}

#URL
URL_first = 'https://sh.lianjia.com/ershoufang/'

#获取网页原始数据
def download_page(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path='D:/chromedriver.exe',chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(url)
    data = driver.page_source
    return data

#从网页中提取感兴趣文本
def get_information(doc,last_page):
    soup= BeautifulSoup(doc, 'html.parser')
    content = soup.find('ul', attrs={'class': 'sellListContent'})
    keywords  =[]
    location2s = []
    names = []
    totalprices = []
    unitprices = []
    spaces = []
    fans = []
    p_list = []
    for i in content.find_all('li', attrs={'class': 'clear'}):
        details = i.find('div', attrs={'class': 'info'})

        #关键词
        flag = details.find('div', attrs={'class':'title'})
        keyword = flag.find('a').get_text()
        #区域划分
        flag = details.find('div',attrs={'class':'positionInfo'})
        location23 = []
        for f in flag.find_all('a'):
            location23.append(f.get_text())
        #获取总价格
        price = details.find('div',attrs={'class':'priceInfo'})
        totalprice = price.find('div',attrs={'class':'totalPrice'})
        totalprice = totalprice.find('span').get_text()
        #获取单价
        unitprice = price.find('div', attrs={'class': 'unitPrice'})
        unitprice = unitprice.find('span').get_text()
        #获取空间
        space = details.find('div',attrs={'class':'houseInfo'}).get_text()
        #获取关注人数
        fan = details.find('div',attrs={'class':'followInfo'}).get_text()

        unitprice = unitprice.split('元')[0].split('价')[1]
        space = space.split('|')[1].strip().split('平')[0]
        fan = fan.split('/')[0].strip().split('人')[0]

        keywords.append(keyword)
        names.append(location23[0])
        location2s.append(location23[1])
        totalprices.append(totalprice)
        unitprices.append(unitprice)
        spaces.append(space)
        fans.append(fan)
        #print(keyword,location23[0],location23[1],totalprice,unitprice,space,fan)
    if last_page == 1:
        pagelist = soup.find('div', attrs={'class': 'contentBottom'})
        pagelist = pagelist.find('div', attrs={'class': 'page-box'})
        for p in pagelist.find_all('a'):
            p_list.append(p.get_text())
        last_page = int(p_list[-2])

    return keywords,names,location2s,totalprices,unitprices,spaces,fans,last_page

for location_name in tqdm(house_dict):
    location_pingyin = house_dict[location_name]
    current_page = 1
    last_page = 1

    keywords = []
    location2s = []
    names = []
    totalprices = []
    unitprices = []
    spaces = []
    fans = []
    while current_page <= 10:
        if current_page==1:
            url = URL_first + location_pingyin + '/'
            print('当前爬取的网页网址为：'+ url)
            doc = download_page(url)
            keyword, name, location2, totalprice, unitprice, space, fan, last_page = get_information(doc,last_page)

            keywords += keyword
            names += name
            location2s += location2
            totalprices += totalprice
            unitprices += unitprice
            spaces += space
            fans += fan
            print('该区域共有' + str(last_page) + '页信息爬取')
            current_page += 1
        else:
            url = URL_first + location_pingyin + '/' + 'pg' + str(current_page) + '/'
            print('共'+str(last_page)+'页，当前爬取第'+str(current_page)+'页')
            current_page += 1

            print('当前爬取的网页网址为：' + url)

            doc = download_page(url)
            keyword, name, location2, totalprice, unitprice, space, fan, last_page = get_information(doc, last_page)

            keywords += keyword
            names += name
            location2s += location2
            totalprices += totalprice
            unitprices += unitprice
            spaces += space
            fans += fan

    data = [keywords, names, location2s, totalprices, unitprices, spaces, fans]

    data_csv = DataFrame(data, index=['keyword', 'name', 'location2', 'totalprice', 'unitprice', 'space', 'fan'],
                         columns=np.array(range(len(names))))
    data_csv = data_csv.T
    data_csv['location'] = location_name
    data_csv.to_csv('data/' + location_name + '.csv', index=False)
