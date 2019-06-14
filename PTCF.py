# -*- coding: UTF-8 -*-

from __future__ import division#使除法运算可以得到小数点位数
import datetime
import time

from data import *
from data2 import * 
from similarity import *
from INITCF import *
from SPCF2 import *
from TIMECF2 import *

'''
PTCF设计思路
目标:依据不同阶段的数据量，选择不同推荐方式，推荐个数为10
流程： 1.计算评分记录数的比重
       2.已经该用户的比重选择推荐方案
            初始阶段：ratio∈(0,Ra) 方案1
            稀疏阶段：ratio∈(Ra，Rb) 方案2
            丰富阶段：ratio∈(Rb，+∞) 方案3
       3.返回推荐结果
'''

def PTCF(prefs,prefs_time,person,n=12,Ra=0.0005,Rb=0.001):#8 // 17

    item_count = len(transformPrefs(prefs))#物品总数
    rating_count = len(prefs[person])#待推荐用户的评分总数
    ratio =  rating_count/item_count#待推荐用户的评分比重

    if ratio <= Ra:
        rankings = INITCF(prefs,person,n)#未看过的评分最高：体现了个性化推荐
    elif ratio <= Rb:
        rankings = SPCF3(prefs,person,n)#方案2
    else:
        rankings = TIMECF(prefs,prefs_time,person,n)#方案2

    return rankings

#测试
if __name__ == "__main__":
    
    #1.在图书数据集GoodBook上

    #2.在电影数据集MovieLens上