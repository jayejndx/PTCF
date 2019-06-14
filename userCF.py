# -*- coding: UTF-8 -*-
#user_CF

from __future__ import division
from math import sqrt

from data import *
from data2 import *
from similarity import *


#寻找相似邻居
def topMatches(prefs,person,n=5,similarity=sim_distance):
    scores=[(similarity(prefs,person,other),other)
            for other in prefs if other!=person]#当前用户与其他用户的相似度集合

    scores.sort()#升序
    scores.reverse()#降序
    return scores[0:n]#取两者相似度靠前的前n位


#基于用户的推荐
def getRecommendedUser(prefs,person,n=30,similarity=sim_distance):

    #1.基于用户的值汇总
    totals={}#评分值之和
    simSums={}#相似度之和
    for other in prefs:#1.基于用户
        
        #不和自己比较 
        if other==person: continue       
        sim=similarity(prefs,person,other)#两用户相似度---在线       
        if sim<=0: continue#忽略评价值<=0情况-》剩下的都是相似用户
        
        for item in prefs[other]:
            #只对当前用户未看的物品进行评价
            if item not in prefs[person] or prefs[person][item]==0:
                #相似度*评价值
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim#其它用户对该物品的评分*两用户的相似度（在线：调方法）
                #对电影item评过分用户的相似度之和，视不同物品而不同
                simSums.setdefault(item,0)
                simSums[item]+=sim
       
    #2.建立归一化列表
    rankings=[(total/simSums[item],item) for item,total in totals.items()]
        
    #3.排序
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]


            
#测试 
if __name__ == "__main__":

    
