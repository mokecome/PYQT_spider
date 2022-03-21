# -*- coding: utf-8 -*-
"""
Created on Mon May  3 08:46:57 2021

@author: Bill
"""
import os
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import jieba
import matplotlib.pyplot as plt
import seaborn as sns
import wordcloud
from wordcloud import ImageColorGenerator
import PIL.Image as Image
from UI import  Ui_MainWindow




def strcut_word(text):#中文利用jieba.cut進行分詞 #長的評論先萃取
    return " ".join(list(jieba.cut(text)))          #dataFrame  gdata_1['content'].apply(lambda x: " ".join(list(jieba.analyse.extract_tags(x,topK=10)))) 



def filecut_words(file_path):  
 
    text_with_spaces = ''
    text = open(file_path,'r',encoding='utf-8').read() #每個類別的txt
    text_cut = jieba.cut(text)
    for word in text_cut:
        text_with_spaces += word + ' '

    return text_with_spaces       #  '我今天很高兴'  ['今天','高兴']   '今天 高兴'
def loadfile(file_dir,label):  #處理不同類別
    """
    加载路径下所有文件
    :return:
    """
    if not os.path.exists(file_dir): # 判断当前项目文件路径下没有 "三寸人间" 这个文件夹
        os.mkdir(file_dir)
    file_list = os.listdir(file_dir)#file_dir
    #正則
    word_list = []
    labels_list = []#如果下載多項
    #labels_list_no=[]
    
    for file in file_list:
        file_path = file_dir + '/' + file
        word_list.append(filecut_words(file_path))
        labels_list.append(label)
        
        #labels_list_no(file[0:12])  #索引 函數 # 分割字符取下標  #正則提取
    
    return  word_list,labels_list


def tfidf_demo(train_words_list1): #傳入列表 labels_list_no
  

    stop_words = open('stopword.txt', 'r', encoding='utf-8').read()
    stop_words = stop_words.encode('utf-8').decode('utf-8-sig') # 列表头部\ufeff处理
    stop_words = stop_words.split('\n') # 根据分隔符分隔
   #1.實例化一個轉換器類
    tf = TfidfVectorizer(stop_words=stop_words,max_df=0.5)
    train_features = tf.fit_transform(train_words_list1) #列表 
   #2.調用fit_transform()
    data_final=tf.fit_transform(train_words_list1)
    print("train_words_list1:\n",data_final.toarray()) #沒有sparse參數 直接.toarray()
    print("特徵名字:\n",tf.get_feature_names())

    w=wordcloud.WordCloud(background_color="white", 
                      width=1000, 
                      height=700, 
                      scale=15, 
                      font_path='msyh.ttc',
                      stopwords=stop_words,
                      contour_color="red",
                      contour_width=5
                     )
 
      
    w.generate(str(train_words_list1))
    if not os.path.exists('img'): # 判断当前项目文件路径下没有 "" 这个文件夹
        os.mkdir('img')
    w.to_file('img/'+'all.png')       


