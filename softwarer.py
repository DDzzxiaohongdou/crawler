#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: DDZZxiaohongdou 2020/4/6 completed

from pandas import DataFrame
import time
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from tkinter import *
import os
import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from terminaltables import AsciiTable
from tkinter import scrolledtext
import tkinter as tk
from matplotlib.pylab import mpl

#from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def work_cloud_visualization():
    global company_name
    data = pd.read_csv(company_name)
    data.sort_values(by='fan', inplace=True, ascending=False)
    data.reset_index(inplace=True)
    data = data.loc[0:100, :]
    words = ''
    word_list = []
    girl_image = plt.imread('girl.jpg')
    wc = WordCloud(background_color='white',  # 背景颜色
                   max_words=1000,  # 最大词数
                   mask= girl_image,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
                   max_font_size=100,  # 显示字体的最大值
                   font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
                   random_state=42,  # 为每个词返回一个PIL颜色
                   # width=1000,  # 图片的宽
                   # height=860  #图片的长
                   )
    for i in data.name:
        words = words + i
    word_generator = jieba.cut(words, cut_all=False)
    for word in word_generator:
        word_list.append(word)
    text = ' '.join(word_list)
    wc.generate(text)
    # 基于彩色图像生成相应彩色
    image_colors = ImageColorGenerator(girl_image)
    # 显示图片
    plt.imshow(wc)
    # 关闭坐标轴
    plt.axis('off')
    # 绘制词云
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis('off')
    wc.to_file('19th.png')
    plt.show()

def data_analyse_button1():
    global company_name
    data = pd.read_csv(company_name)
    data.sort_values(by='fan',inplace=True,ascending=False)
    data.reset_index(inplace=True)
    data = data.loc[0:10,:]
    inquire = data
    head = list(inquire)
    data_inquire = [head]
    content = inquire.values.tolist()
    for i in range(len(content)):
        data_inquire.append(content[i])
    data_inquire = AsciiTable(data_inquire)
    text.insert(INSERT, data_inquire.table)
    data = data.loc[:,['totalprice','fan','name']]
    data.set_index('name',inplace=True)
    print(data)
    data.plot(kind='bar')
    plt.show()

def data_analyse_button2():
    global company_name
    data = pd.read_csv(company_name)
    data.sort_values(by='fan', inplace=True, ascending=False)
    data.reset_index(inplace=True)
    inquire = data
    head = list(inquire)
    data_inquire = [head]
    content = inquire.values.tolist()
    for i in range(len(content)):
        data_inquire.append(content[i])
    data_inquire = AsciiTable(data_inquire)
    text.insert(INSERT, data_inquire.table)
    data['location'].value_counts().plot(kind='bar')
    plt.show()

def data_analyse_button3():
    global company_name
    data = pd.read_csv(company_name)
    data.sort_values(by='fan', inplace=True, ascending=False)
    data.reset_index(inplace=True)
    inquire = data
    head = list(inquire)
    data_inquire = [head]
    content = inquire.values.tolist()
    for i in range(len(content)):
        data_inquire.append(content[i])
    data_inquire = AsciiTable(data_inquire)
    text.insert(INSERT, data_inquire.table)
    data['location'].value_counts().plot(kind='pie')
    plt.show()

def data_analyse_button4():
    global company_name
    data = pd.read_csv(company_name)
    inquire = data
    head = list(inquire)
    data_inquire = [head]
    content = inquire.values.tolist()
    for i in range(len(content)):
        data_inquire.append(content[i])
    data_inquire = AsciiTable(data_inquire)
    text.insert(INSERT, data_inquire.table)
    data['unitprice'].hist(bins=50)
    plt.show()

def data_analyse_button5():
    global company_name
    data = pd.read_csv(company_name)
    inquire = data
    head = list(inquire)
    data_inquire = [head]
    content = inquire.values.tolist()
    for i in range(len(content)):
        data_inquire.append(content[i])
    data_inquire = AsciiTable(data_inquire)
    text.insert(INSERT, data_inquire.table)
    data['totalprice'].hist(bins=50)
    plt.show()

def data_inquire_entry(event=None):
    global company_name
    if company_name == '':
        text.insert(INSERT, '请在分析前输入网址名称')
    data = pd.read_csv(company_name)
    temp1 = e1.get()  # 区名
    temp2 = e2.get()  # 居住圈名
    temp3 = e3.get()  # 小区名
    temp4 = e4.get()  # 总价左
    temp5 = e5.get()  # 总价右
    temp6 = e6.get()  # 单价左
    temp7 = e7.get()  # 单价右
    temp8 = e8.get()  # 空间左
    temp9 = e9.get()  # 空间右

    #非数字类型的筛选
    dict = {temp1: 'location', temp2: 'location2', temp3: 'name'}
    for i in dict:
        if i == '':
            continue
        else:
            data = data[data[dict[i]] == i]
    #总价格筛选
    if temp4 != '':
        data = data[data['totalprice'] > float(temp4)]
    if temp5 != '':
        data = data[data['totalprice'] < float(temp5)]
    else:
        pass
    #单价格筛选
    if temp6 != '':
        data = data[data['unitprice'] > float(temp6)]
    if temp7 != '':
        data = data[data['unitprice'] < float(temp7)]
    else:
        pass
    #空间筛选
    if temp8 != '':
        data = data[data['space'] > float(temp8)]
    if temp9 != '':
        data = data[data['space'] < float(temp9)]
    else:
        pass

    inquire = data
    head = list(inquire)
    data_inquire = [head]
    content = inquire.values.tolist()
    for i in range(len(content)):
        data_inquire.append(content[i])
    data_inquire = AsciiTable(data_inquire)
    text.insert(INSERT, data_inquire.table)

def update():
    text.delete(1.0, tk.END)

company_name = ''

def get_company_name(event=None):
    global company_name
    company_name = e10.get()
    if company_name == '':
        text.insert(INSERT, '请在分析前输入网址名称')
    else:
        company_name = company_name + '.csv'
        time.sleep(3)
        text.insert(INSERT, '数据读取成功')

root = Tk()
root.title('哈尔滨房价分析系统')
root.minsize(800, 500)
label_analyse = Label(root, text='请输入分析网址名称', background='red').grid(row=0,column=0,padx=50)

e10 = StringVar()
en10 = Entry(root, validate='key', textvariable=e10)
en10.grid(row=0, column=1)
en10.bind('<Return>', get_company_name)

inquire_label1 = Label(root, text='查询模块', background='red').grid(row=1,column=0,pady=5)
inquire_label2 = Label(root, text='请输入区名').grid(row=2,column=0,pady=5)
inquire_label3 = Label(root, text='请输入居住圈名').grid(row=3,column=0,pady=5)
inquire_label4 = Label(root, text='请输入小区名').grid(row=4,column=0,pady=5)
inquire_label5 = Label(root, text='请输入总价区间').grid(row=5,column=0,pady=5)
inquire_label6 = Label(root, text='请输入单价区间').grid(row=6,column=0,pady=5)
inquire_label7 = Label(root, text='请输入空间区间').grid(row=7,column=0,pady=5)


#数据查询输入模块
#区名
e1 = StringVar()
en1 = Entry(root, validate='key', textvariable=e1)
en1.grid(row=2, column=1)
en1.bind('<Return>', data_inquire_entry)
#居住圈名
e2 = StringVar()
en2 = Entry(root, validate='key', textvariable=e2)
en2.grid(row=3, column=1)
en2.bind('<Return>', data_inquire_entry)
#小区名
e3 = StringVar()
en3 = Entry(root, validate='key', textvariable=e3)
en3.grid(row=4, column=1)
en3.bind('<Return>', data_inquire_entry)
#总价区间
e4 = StringVar()
en4 = Entry(root, validate='key', textvariable=e4)
en4.grid(row=5, column=1)
en4.bind('<Return>', data_inquire_entry)
e5 = StringVar()
en5 = Entry(root, validate='key', textvariable=e5)
en5.grid(row=5, column=2)
en5.bind('<Return>', data_inquire_entry)
#单价区间
e6 = StringVar()
en6 = Entry(root, validate='key', textvariable=e6)
en6.grid(row=6, column=1)
en6.bind('<Return>', data_inquire_entry)
e7 = StringVar()
en7 = Entry(root, validate='key', textvariable=e7)
en7.grid(row=6, column=2)
en7.bind('<Return>', data_inquire_entry)
#空间区间
e8 = StringVar()
en8 = Entry(root, validate='key', textvariable=e8)
en8.grid(row=7, column=1)
en8.bind('<Return>', data_inquire_entry)
e9 = StringVar()
en9 = Entry(root, validate='key', textvariable=e9)
en9.grid(row=7, column=2)
en9.bind('<Return>', data_inquire_entry)

#数据展示
inquire_label8 = Label(root, text='分析模块', background='red').grid(row=1,column=3,pady=10)

anaylse_button1 = Button(root, text='最受欢迎TOP10房源',command = lambda: data_analyse_button1()).grid(row=2,column=3,pady=5)
anaylse_button2 = Button(root, text='行政区房源数分布柱状图',command=  lambda: data_analyse_button2()).grid(row=3,column=3,pady=5)
anaylse_button3 = Button(root, text='行政区房源数分布饼状图',command = lambda: data_analyse_button3()).grid(row=4,column=3,pady=5)
anaylse_button4 = Button(root, text='哈尔滨房源均价直方图',command = lambda: data_analyse_button4()).grid(row=5,column=3,pady=5)
anaylse_button5 = Button(root, text='哈尔滨房源总价直方图',command = lambda: data_analyse_button5()).grid(row=6,column=3,pady=5)
anaylse_button6 = Button(root, text='受欢迎房源词云图',command = lambda: work_cloud_visualization()).grid(row=7,column=3,pady=5)

# 数据显示模块
text = scrolledtext.ScrolledText(root, width=150, height=20)
text.grid(row=8, columnspan=8,padx=20,pady=10)

clear_button = Button(root, text='清空', command=lambda: update()).grid(row=9,column=1)

root.mainloop()