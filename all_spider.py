# -*- coding: utf-8 -*-
"""
Created on Thu May  6 08:07:41 2021

@author: Bill
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
import time  # 内置模块, 时间
import csv  # 保存csv数据的模块, 内置模块
import numpy as np
import pandas as pd
from tfidf import filecut_words,loadfile,tfidf_demo
from ten import change_word,Commoditypopularity,get_data,count_comment
import json
import requests
import concurrent.futures 
import logging
from datetime import datetime
import random  # 随机数

#from constants import TAO_USERNAME, TAO_PASSWORD
'''
#避免循環導入
def circular_import_print(s):
    from UI_C import  MainWindow
    MainWindow.printf(s)
'''
def JD_spider(word,total_pages,ui):#css 動態加載執行JS
    ChromeOptions = webdriver.ChromeOptions()
    ChromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(options=ChromeOptions)
    driver.get('https://www.jd.com/')
    WebDriverWait(driver, 5, 0.5).until(lambda x: x.find_element_by_css_selector('#key'))
    #商品搜索(输入关键字, 点击搜索按钮)-------------------------get_product(word)
    driver.find_element_by_css_selector('#key').send_keys(word)
    driver.find_element_by_id('search-btn').click()

    driver.maximize_window() # 最大化浏览器
    driver.implicitly_wait(10)  # 隐式等待 智能化的等待
    #---------------------------------------------------
    
    time_1 = time.time()
    
    for page in range(total_pages): # 100次商品頁數  資料擷取
        # 数据在页面中有懒加载----------------------------------------------------------def drop_down():
        for i in range(1, 11, 2):  # 13579
            time.sleep(0.5)
            j = i / 9  # 1/9  3/9 ... 9/9
            # 根据js(JavaScript)操作页面的下拉操作
            js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
            driver.execute_script(js) 
        #----------------------------------------------------------------------------------------------
        
        #商品的数据解析, 数据保存--------------------------------------------------------------------------------------------def parse_data():
        
        lis = driver.find_elements_by_css_selector('.gl-item')  # 获取所有li标签

        for li in lis:  # 二次提取数据
            try:
                name = li.find_element_by_css_selector('.p-name a em').text
                name = name.replace('京品手机', "").replace('"', '').replace('\n', '')
                price = li.find_element_by_css_selector('div.p-price strong i').text + '元'  # 商品的价格
                deal = li.find_element_by_css_selector('div.p-commit strong a').text  # 商品的评价数量(熱度) 熱度前十的商品
                dealhref=li.find_element_by_css_selector('div.p-commit strong a').get_attribute('href')  # 商品的评价網址
                title = li.find_element_by_css_selector('span.J_im_icon a').get_attribute('title')  # 商品的店铺名字

                print(name, price, deal,dealhref,title, sep=' | ')
                ui.printf(name) 
                with open('京东数据.csv', mode='a', encoding='utf-8', newline='') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow([name, price, deal,dealhref, title])
            except:
                print('解析错误')
         #----------------------------------------------------------------------------------------------------------------------       
                
        #找到下一页标签, 点击-----------------------------------------------------------------------def get_next():
        driver.find_element_by_css_selector('#J_bottomPage > span.p-num > a.pn-next > em').click()
        #-------------------------------------------------------------------------------------------
        
    time_2 = time.time()    
    use_time = int(time_2) - int(time_1)
    print(f'爬蟲总计耗时{use_time}秒')
    ui.printf(f'爬蟲总计耗时{use_time}秒') 
    sortdata,commentdf=Commoditypopularity(total_pages)
    train_words_list1,train_labels1 = loadfile('alldata','十大熱度')
    tfidf_demo(train_words_list1)
    return None
    




if __name__ == '__main__':
   
    word = input('请输入商品的关键字:')
    total_pages=5#評論頁數
    # 创建一个浏览器对象
    
    
    # logging.getLogger('').handlers=[] #spider執行
    # filename='{:%Y-%m-%d}'.format(datetime.now())+'.log'
    # FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    # #DATE_FORMAT = '%Y%m%d %H:%M:%S'
    # logging.basicConfig(filename='a.log',level=logging.DEBUG,format=FORMAT) #預設filemode參數是設為a#開發.DEBUG 上產品.warning #, datefmt=DATE_FORMAT
    
    JD_spider(word,total_pages)
    
       
   
    
    
    sortdata,commentdf=Commoditypopularity(total_pages)
    
 #-------------------------------------------------排程   

    
    train_words_list1,train_labels1 = loadfile('alldata','十大熱度')
    tfidf_demo(train_words_list1)
       
    
    
   
