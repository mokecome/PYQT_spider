# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 19:17:56 2021

@author: Bill
"""
from selenium import webdriver
import numpy as np
import pandas as pd
import json
import requests
from tfidf import filecut_words,loadfile,tfidf_demo

def change_word(word):
    word=str(word).strip("+")
    position = word.find('万')   
    length = len(word)
    if '万' in word:
        commentnum = word[:position]+"0000"
    else:
        commentnum=word[:]
        
   
    return commentnum



def Commoditypopularity(total_page):#商品熱度分析
    data = pd.read_csv('京东数据.csv',encoding='utf-8',engine='python',header=None,prefix='X') 
    data.drop_duplicates(inplace=True)
    data['X2'] = data['X2'].fillna(0)
    data['X5'] = data.X2.apply(change_word)
    data.X5 = data.X5.astype('float')
    sortdata=data.sort_values(by=['X5'],axis=0,ascending=False) #
    sortdata.reset_index(inplace=True)
    sortdata['X6']=sortdata['X5']/sortdata['X5'].sum()
    sortdata['ID']= sortdata['X3'].replace(to_replace={'https://item.jd.com/':''},regex=True).replace(to_replace={'.html#comment':''},regex=True) 
    print(sortdata['ID'][0:10])


    tendata=sortdata['ID'][0:10]
    df1=pd.DataFrame()
    df1allindex=pd.DataFrame()
    #數量
    
    for t in tendata: #前10抓5頁
        
        print('------------------------------------------------------------------------------')

        for page in range(0,total_page):
            test = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
            r1 = requests.get('https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={pid}&score=1&sortType=5&page={p}&pageSize=10&isShadowSku=0&fold=1'.format(pid=t,p=page),headers = test)
            data =json.loads(r1.text[20:-2]).get("comments")
            df = pd.DataFrame(data) #第page頁表格 
            df1=df1.append(df)          #所有頁表格
            df1['PID']=t
            print(df1.content)
        
    
        df1newindex=df1.reset_index(drop=True)
        df1allindex=df1allindex.append(df1newindex)
        df1.drop(df1.index, inplace=True) #清空dataframe
    
    shortdf=df1allindex[['content','creationTime','replyCount','productColor','productSize','PID']] 

    #取值
    
    shortdfgroup=shortdf.groupby('PID')['content']

    for t in tendata:  
        sa=''  
        for s in shortdfgroup.get_group(t):
            sa=sa+s+" "
        
        with open('alldata\\'+t+'.txt', mode='w', encoding='utf-8') as f:
            f.write(sa)  #" ".join(list(shortdfgroup.get_group(t)))
        
    return sortdata,shortdf #返回熱度排序  評論




def get_data(base_url,pid,total_pages):#個別品牌 好評結巴關鍵字
    df1=pd.DataFrame()
    for p in range(0,total_pages):
        test = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        r1 = requests.get(base_url.format(pid=pid,p=p),headers = test)
        data =json.loads(r1.text[20:-2]).get("comments")#返回列表   response.json()[20:-2]).get("comments")
        df = pd.DataFrame(data) #第page頁表格 
        df1=df1.append(df)          #所有頁表格
        df1['PID']=pid
        print(df1.content)

    
    dfnewindex=df1.reset_index(drop=True)
    returndf=dfnewindex[['content','creationTime','productColor','productSize','PID','referenceName','replyCount']] 
    returndf['creationTime']= pd.to_datetime(returndf['creationTime'])#先轉換才能設index
    returndf.set_index('creationTime', inplace=True)
    
    return returndf

def count_comment(data_1):
    data_1['PID']=1
    countdata_1=data_1.resample('D').sum()
    countdata_1['count'] = countdata_1.apply(lambda x: x['PID'] +  x['replyCount'], axis=1)
    print(countdata_1)
    return countdata_1 # countdata_1['count']總討論數  countdata_1['replyCount'] 回文數   
    

