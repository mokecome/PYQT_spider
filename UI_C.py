# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 17:31:20 2022

@author: Bill
"""

from PyQt5 import QtWidgets, QtCore
from UI import  Ui_MainWindow
from PyQt5.QtGui import QImage, QPixmap
import all_spider
import time


import cv2
import glob
import shutil, os
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        #

    def setup_control(self):
        self.ui.pushButton.clicked.connect(self.buttonClicked)  #連接執行
        self.ui.pushButton_2.clicked.connect(self.buttonClicked2)  #連接執行
        self.img_path = 'show.png'
        self.display_img()
        self.count=0
        
        #改變主文字
    def display_img(self):
        self.img = cv2.imread(self.img_path)
        self.img =cv2.resize(self.img,(750,550))
        height, width, channel = self.img.shape
        bytesPerline =3* width
        self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.ui.label.setPixmap(QPixmap.fromImage(self.qimg))
        self.ui.label.adjustSize()
        
    
    

    def buttonClicked(self):
       
        word=self.ui.lineEdit.text()
        page=self.ui.lineEdit_2.text()
        time_1 = time.time()
        all_spider.JD_spider(word,int(page),self.ui) #抓幾頁  抓過得可用時間排除
        time_2 = time.time()
        use_time = int(time_2) - int(time_1)
        
        self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End) 
        self.ui.textBrowser.append(f'資料處理总计耗时{use_time}秒')
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
    def buttonClicked2(self):
        self.img_path='show.png'
        self.display_img() 
        myfiles = glob.glob('img' + '/*.png')  #讀取資料夾全部jpg檔案
        self.img_path = 'img'+'/'+myfiles[self.count]
        self.display_img() 
   

        self.count=self.count+1
        self.count=self.count%len(myfiles)
        
      
import sys
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
