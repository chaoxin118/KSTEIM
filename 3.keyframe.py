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
Path_11='D:\\能量场mat\\'
PATH_2='D:\\30帧\\'


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
N=30    # 关键帧数量
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
        
        Diff=zeros((h,w))
        Diff1=zeros((h,w))
        Diff2=zeros((h,w))
        List1=[]
        diff=diff1=diff2=0
        
        if(f<=N):
            depth1=zeros((h,w,f))
            for ff in range(f):
                depth1[:,:,ff]=depth[:,:,ff]
            sio.savemat(path_2,{'depth1':depth1})
        while(f>N):
            for i in range(f-N):
                depth1=zeros((h,w,f-1))
                for ff in range(f-1):
                    b=ff
                    Diff=abs(depth[:,:,ff+1]-depth[:,:,ff])
                    diff=np.linalg.norm(Diff,ord=2)
                    # for hh in range(h):
                    #     for ww in range(w):
                    #         diff=Diff[hh][ww]+diff
                    List1.append((b,diff))
                #找出最小值对应的索引
                List1=sorted(List1,key=lambda x:(x[1],x[0]))
                a=List1[0][0]
                #print(a)
                
                if(a==0):
                    for ff in range(0,a+1):
                        depth1[:,:,ff]=depth[:,:,ff]
                    for ff in range(a+1,f-1):
                        depth1[:,:,ff]=depth[:,:,ff+1]
                elif(a==len(List1)-1):
                    for ff in range(0,a):
                        depth1[:,:,ff]=depth[:,:,ff]
                    for ff in range(a,f-1):
                        depth1[:,:,ff]=depth[:,:,ff+1]
                else:                                                        
                    Diff1=abs(depth[:,:,a+1]-depth[:,:,a-1])
                    Diff2=abs(depth[:,:,a+2]-depth[:,:,a])
                    diff1=np.linalg.norm(Diff1,ord=2)
                    diff2=np.linalg.norm(Diff2,ord=2)
                    # list2.append(diff1)
                    # list3.append(diff2)
                
                    if(diff1<diff2):
                        for ff in range(0,a):
                            depth1[:,:,ff]=depth[:,:,ff]
                        for ff in range(a,f-1):
                            depth1[:,:,ff]=depth[:,:,ff+1]
                    elif(diff1>diff2):
                        for ff in range(0,a+1):
                            depth1[:,:,ff]=depth[:,:,ff]
                        for ff in range(a+1,f-1):
                            depth1[:,:,ff]=depth[:,:,ff+1]
                print(i)
                List1=[]
                f=f-1
                for ff1 in range (f):
                    depth[:,:,ff1]=depth1[:,:,ff1]
            sio.savemat(path_2,{'depth1':depth1})

        
               

            
           