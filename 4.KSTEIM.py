#牺牲一维的空间信息用时间信息代替。
#用列和来投影
import scipy.io as sio  
from numpy import *  
from PIL import Image#图片处理库
import scipy.io as sio 
import os
import sys
from numpy import * 
import copy#深拷贝
import time
import datetime 
import matplotlib.pyplot as plt #绘图用的模块
from mpl_toolkits.mplot3d import Axes3D #绘制3D坐标的函数
import numpy as np
###############文件地址（相对）########################
#py_length=len(os.path.basename(sys.argv[0]).split(".")[0])
#PATH_R1=sys.argv[0][0:-(py_length+9)]+'微软数据库\MSR-Action3D(深度.mat)'#'.py'占位3
#print(PATH_R1)

##############################规则时自动生成SAMPLE_LISTS

#文件路径
Path_R1='D:\\30\\'
Path_KSTEIM='D:\\人体行为识别研究最新版\\KSTEIM(不做归一化)\\'

def DeepCopy(Objects):#深拷贝

   objects=copy.deepcopy(Objects)

   return objects 
def measure_x(matrix):
    [w,h]=np.shape(matrix)
    column_sum = matrix.sum(axis=0)    #列和 、row
    for i in range(h):
        if(column_sum[i]!=0):
            column_sum[i]=255
    return column_sum
def measure_y(matrix):
    [w,h]=np.shape(matrix)
    column_sum = matrix.sum(axis=1)    #列和 、row
    for i in range(w):
        if(column_sum[i]!=0):
            column_sum[i]=255
    return column_sum

def ROI_array(Array):
    array=DeepCopy(Array)
    h,w=shape(array)
    #print(shape(array))
    
    if(1==1):#宽度轴范围
        w_mim=10000
        w_max=0
        axis_w=array.sum(axis=0)#
        for ww in range(w):#找最小点
            if(ww>w_mim):
                break
            else:
                if(axis_w[ww]!=0):#最小点
                    if(ww<w_mim):
                        w_mim=ww
                    break

        for ww in range(w):#找最大点
            if(w-1-ww<w_max):
                break
            else:
                if(axis_w[w-1-ww]!=0):#最大点
                    if(w-1-ww>w_max):
                        w_max=w-1-ww
                    break
    if(1==1):#高度轴范围
        h_mim=10000
        h_max=0
        axis_h=array.sum(axis=1)#
        for hh in range(h):#找最小点
            if(hh>h_mim):
                break
            else:
                if(axis_h[hh]!=0):#最小点
                    if(hh<h_mim):
                        h_mim=hh
                    break

        for hh in range(h):#找最大点
            if(h-1-hh<h_max):
                break
            else:
                if(axis_h[h-1-hh]!=0):#最大点
                    if(h-1-hh>h_max):
                        h_max=h-1-hh
                    break
    return array[h_mim:h_max,w_mim:w_max]

print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) 
files= os.listdir(Path_R1)
for file in files: #遍历文件夹
    if(file[-3:]=='mat'):
        action=int(file[1:3])
        people=int(file[5:7])
        order=int(file[9:11])
        # print(action)
        # print(people)
        # print(order)
        
        if(action<10):
            sign_a='a0'
        else:
            sign_a='a'

        if(people<10):
            sign_s='_s0'
        else:
            sign_s='_s'
        
        if(order<10):
            sign_e='_e0'
        else:
            sign_e='_e'

        path_KSTEIM=Path_KSTEIM+sign_a+str(action)+sign_s+str(people)+sign_e+str(order)+"_sdepth"#文件夹目录

        #print(Path_R1+"\\"+file)
        data=sio.loadmat(Path_R1+"\\"+file)
        # print(data)
        depth=data['depth']
        h,w,f=shape(depth)
        KSTEIM_w=zeros((f,w))
        KSTEIM_h=zeros((f,h))

        KSTEIM_d=zeros((f,360))
   
        for ff in range(f-1):
            top=zeros((360,w,f))
            side=zeros((h,360,f)) 
            for hh in range(h):
                for ww in range(w):
                    #depth[hh][ww][ff]=int(depth[hh][ww][ff])
                    if(depth[hh][ww][ff]!=0):#只投影有能量点
                        #depth[hh][ww][ff]=depth[hh][ww][ff] 
                        top[int(depth[hh][ww][ff])][int(ww)]=hh#
                        side[int(hh)][int(depth[hh][ww][ff])]=ww

            KSTEIM_w[ff,:]=depth[:,:,ff].sum(axis=0)
            KSTEIM_h[ff,:]=depth[:,:,ff].sum(axis=1)

            KSTEIM_d[ff,:]=top[:,:,ff].sum(axis=1)

            KSTEIM_w=ROI_array(KSTEIM_w)
            KSTEIM_h=ROI_array(KSTEIM_h)
            KSTEIM_d=ROI_array(KSTEIM_d)

        # 归一化到0-300
        KSTEIM_w=KSTEIM_w*255/amax(KSTEIM_w)
        KSTEIM_h=KSTEIM_h*255/amax(KSTEIM_h)
        KSTEIM_d=KSTEIM_d*255/amax(KSTEIM_d)
     
        KSTEIM_w = Image.fromarray(array(KSTEIM_w))#
        KSTEIM_w = KSTEIM_w.convert('L')
        # KSTEIM_w = KSTEIM_w.resize((240, 30))
        KSTEIM_w.save(path_KSTEIM+'_w.png')
        
        KSTEIM_h = Image.fromarray(array(KSTEIM_h))#
        KSTEIM_h = KSTEIM_h.convert('L')
        # KSTEIM_h = KSTEIM_h.resize((240, 30))
        KSTEIM_h.save(path_KSTEIM+'_h.png')
        
        KSTEIM_d = Image.fromarray(array(KSTEIM_d))#
        KSTEIM_d = KSTEIM_d.convert('L')
        # KSTEIM_d = KSTEIM_d.resize((360, 30))
        KSTEIM_d.save(path_KSTEIM+'_d.png')

print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))        
        



        