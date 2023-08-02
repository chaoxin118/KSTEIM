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
import numpy as np
###############文件地址（相对）########################
py_length=len(os.path.basename(sys.argv[0]).split(".")[0])
#PATH_R1=sys.argv[0][0:-(py_length+9)]+'微软数据库\MSR-Action3D(深度.mat)'#'.py'占位3
Path_11='D:\\灰度图\\'       # 深度图mat文件，提前将灰度图归一化至0-255
PATH_2='D:\\能量场mat\\'


def DeepCopy(Objects):#深拷贝

   objects=copy.deepcopy(Objects)

   return objects 
def histeq(im,nbr_bins = 256):
    """对一幅灰度图像进行直方图均衡化"""
    #计算图像的直方图
    #在numpy中，也提供了一个计算直方图的函数histogram(),第一个返回的是直方图的统计量，第二个为每个bins的中间值
    imhist,bins = histogram(im.flatten(),nbr_bins,normed= True)
    cdf = imhist.cumsum()   #
    cdf = 255.0 * cdf / cdf[-1]
    #使用累积分布函数的线性插值，计算新的像素值
    im2 = interp(im.flatten(),bins[:-1],cdf)
    return im2.reshape(im.shape),cdf
files= os.listdir(Path_11)
for file in files: #遍历文件夹
    if(file[-3:]=='mat'):
        action=int(file[1:3])
        people=int(file[5:7])
        order=int(file[9:11])
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

        path_2=PATH_2+sign_a+str(action)+sign_s+str(people)+sign_e+str(order)+"_sdepth.mat"#文件夹目录
        data=sio.loadmat(Path_11+"\\"+file)
        # print(data)
        depth=data['depth']
        h,w,f=shape(depth)
        Ene=zeros((1,w))
        List1=[]
        depth_max=0
        depth_min=1000
        A=sum1=sum2=0
        B=0

        for ff in range(0,1):
            for hh in range(h):
                for ww in range(w):
                    sum1=sum1+depth[hh][ww][ff]
        A=sum1/2
        for ff in range(0,1):
            Ene=depth[:,:,ff].sum(axis=0)
            for ww in range(w):
                List1.append((ww,Ene[ww]))
        
        for i in range(0,len(List1)):
            sum2=sum2+List1[i][1]
            if(sum2>=A):
                break
        B=i

        for ff in range(f):
            for hh in range(h):#
                for ww in range(w):
                    if(depth[hh][ww][ff]!=0):
                        depth[hh][ww][ff]=abs(255-depth[hh][ww][ff])+abs(ww-B+1)#取能量场
                   
        # for ff in range(f):
        #     for hh in range(h):#
        #         for ww in range(w):
        #             if(depth[hh][ww][ff]!=0):
        #                 if(depth[hh][ww][ff]>depth_max):
        #                     depth_max=depth[hh][ww][ff]
        #                 if(depth[hh][ww][ff]<depth_min):
        #                     depth_min=depth[hh][ww][ff]
        # for ff in range(f):
        #     for hh in range(h):#
        #         for ww in range(w):
        #             if(depth[hh][ww][ff]!=0):
        #                 depth[hh][ww][ff]=(depth[hh][ww][ff]-depth_min)*255/(depth_max-depth_min) #能量场归一化
        depth[:,B:B+1,:]=255#中轴线

    sio.savemat(path_2,{'depth':depth})
        