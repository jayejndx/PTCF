# -*- coding: UTF-8 -*-

from __future__ import division#使除法运算可以得到小数点位数
import datetime
import time

from data import *
from data2 import *
from similarity import *


#初始推荐
#当前方案：将用户未评分且其他用户评分最高的物品推荐出来
#提高方案:分析用户+匹配物品 ==》个性化
def INITCF(prefs,user,n=10):
    
    #物品-用户矩阵
    itemPrefs = transformPrefs(prefs)

    #用户已评分物品
    Iu = []
    for i in prefs[user]:
        Iu.append(i)

    #用户未评分物品
    Candidate = []
    for i in itemPrefs:
        if i in Iu:continue
        Candidate.append(i)
         
    #推荐列表
    rankings = []
    for c in Candidate:
        ratings = 0
        count = 0
        for i in itemPrefs[c].values():
            ratings += i
            count += 1
        rankings.append((ratings/count,c))
         
    #排序，评分较高者在前
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]


#测试
if __name__ == "__main__":

    '''
    m = loadMovieLens()
    r = InitCF(m,'88',30)
    print r
    '''

    a,b=loaddata()
    r=InitCF(a,'9856',12)
    print(r)
    
