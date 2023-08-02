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
Path_11='D:\\depth\\'   # 原始文件
PATH_2='D:\\灰度图\\'


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
        depth1=data['depth1']
        h,w,f=shape(depth1)
        depth=zeros((h,w,f))
        depth=depth1[:,:,:]
        Ene=zeros((1,w))
        List1=[]
        depth_max1=depth_max2=0
        depth_min1=depth_min2=1000

        for ff in range(f):
            for hh in range(h):#
                for ww in range(w):
                    if(depth[hh][ww][ff]!=0):
                        # if(depth[hh][ww][ff]>depth_max1):
                        #     depth_max1=depth[hh][ww][ff]
                        # if(depth[hh][ww][ff]<depth_min1):
                        #     depth_min1=depth[hh][ww][ff]
                        depth[hh][ww][ff]=(depth[hh][ww][ff]-285)*255/(655-285)   # (depth-min)*255/(max-min)
                    #depth[hh][ww][ff]=abs(255-depth[hh][ww][ff])+abs(ww-a+1)
        D=zeros((h,240,f))
        D=depth[:,20:260,:]
        depth=D

    sio.savemat(path_2,{'depth':depth})
        