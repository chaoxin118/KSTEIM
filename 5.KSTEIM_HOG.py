#!usr/bin/env python
# -*- coding: utf-8 -*-
from skimage.transform import rotate
from skimage.feature import local_binary_pattern
from skimage import data, io
from skimage.color import label2rgb
import skimage
from skimage import feature as ft
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy.io as sio
from numpy import *
from PIL import Image  # 图片处理库
import scipy.io as sio
import os
import sys
from numpy import *
import copy  # 深拷贝
import time
import re
import numpy as np

def tiqu(totalCount):
    totalCount = re.sub("\D", "", totalCount)
    return int(totalCount)

PATH2 = 'D:\\KSTEIM\\'  # 原文件夹地址 ==>DMM_HOG（截图+归一化+膨胀）
files = os.listdir(PATH2)
if (1 == 1):
    x = []
    y = []
    ff = []
    for ii in range(len(files)):
        # for ii in range(2):
        # ii=0

        file_split = files[ii].split("_")  # 命名文件名
        name = tiqu(file_split[0])

        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))  # 作用是格式化时间戳为本地的时间
        print(ii)

        ####################################宽
        if "_d" in files[ii]:
            #print(PATH2 +files[ii])
            im = Image.open(PATH2 +files[ii])
            im = im.resize((120,30))
            features1, m1 = ft.hog(image=im, pixels_per_cell=(10, 10), cells_per_block=(2, 2),
                                   visualise=True)  # 步长为一个cell，滑动块数*cells_per_block*9
            ff = ff + list(features1)
        if "_h" in files[ii]:
            im = Image.open(PATH2 +files[ii])
            im = im.resize((150,30))  # (宽，高)
            features1, m1 = ft.hog(image=im, pixels_per_cell=(10, 10), cells_per_block=(2, 2),
                                   visualise=True)  # 步长为一个cell，滑动块数*cells_per_block*9
            ff = ff + list(features1)
            y.append(name)
        if "_w" in files[ii]:
            im = Image.open(PATH2 +files[ii])
            im = im.resize((100,60))  # (宽，高)
            features1, m1 = ft.hog(image=im, pixels_per_cell=(10, 10), cells_per_block=(2, 2),
                                   visualise=True)  # 步长为一个cell，滑动块数*cells_per_block*9
            ff = ff + list(features1)
            x.append(ff)
            ff = []
            
    print(shape(x))

    sio.savemat('D:\\HOG_features_X.mat',{'X':x})
    sio.savemat('D:\\HOG_features_Y.mat',{'Y':y})

