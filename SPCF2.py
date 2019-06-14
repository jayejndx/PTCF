# -*- coding=UTF-8 -*-
#sp_CF

from __future__ import division
import json
import numpy as np
import pandas as pd
import csv

from data import *
from similarity import *
from userCF import *
from itemCF import *

#基于相似度传播技术的实现
#相似度传播思想:对用户u进行推荐，除了依据u的近邻v，获取v的第一个近邻v1,将v1也视为u的近邻，依据v1获取近邻v2并视为u的近邻，以此类推...


#1.寻找最近邻居
def getTrans(prefs,user):
     
     user_trans = []#目标用户的邻居集合
     
     for p in prefs:
          if p==user:continue
          for item in prefs[user]: 
               if item in prefs[p]:
                    user_trans.append(p)
                    
     return user_trans


#2.寻找邻居集合
#prefs:偏好矩阵
#user:目标用户
#h:迭代次数，h=0:本身，h=1:最近邻居，h=2:最近邻居+最近邻居的邻居，以此类推   
def Trans(prefs,user,h=10):

     user_trans = [user]#目标用户的邻居集合

     #1.h=0
     if h == 0:return user_trans

     #2.迭代：邻居的邻居
     while h>0 :
          trans_h = []
          for u in user_trans:
               trans_h += getTrans(prefs,u)
          user_trans = list(set(user_trans+trans_h));
          if len(user_trans)>60:break;#控制邻居个数在60以内
          h=h-1

     return user_trans[0:60]#据论文结论：邻居个数为60效果最佳

              
#3.相似度计算---核心方法
#！！！但是，还有一种理解，计算两者相似度用传统方法，在评分预测值上下功夫（邻居的邻居的评分值*相似度---这个相似度是待推荐用户与邻居的邻居的相似度，但值有意义吗？）

#prefs:偏好矩阵
#user1,user2:比较对象
#h：迭代次数，论文结论给出最优值为10
#C（0<C<1）：置信系数or阻尼系数：表示相似度随迭代次数增加的传播衰减率，设为0.6(论文没给出)
#similarity：就用传统的皮尔逊（到这里的计算确实用到邻居的邻居的评分，但会不会太作？）
def simTrans(prefs,user1,user2,h=10,C=0.6,similarity=sim_distance):

     if h == 0:return similarity(prefs,user1,user2)

     #邻居集合
     user_trans1 = Trans(prefs,user1,h)
     if user2 in user_trans1:
          user_trans1.remove(user2)#去掉user2，防止后面和自己比较相似度
     user_trans2 = Trans(prefs,user2,h)
     if user1 in user_trans2:
          user_trans2.remove(user1)

     #相似度之和
     simSum1 = 0
     simSum2 = 0
     for u in user_trans2:
          simSum1 += similarity(prefs,user1,u)
     for v in user_trans1:
          simSum2 += similarity(prefs,user2,u)

     #simTrans算出的相似度
     sim = (simSum1/len(user_trans2) + simSum2/len(user_trans1))/2*C
     if sim<0: sim = 0
     return sim
    
     
#4.推荐1:直接调标准CF,评分预测用传统方法
def spCF1(prefs,item,n=30,similarity=simTrans):

     rankings = []#评分预测列表

     #1.基于用户
     ranking_user = getRecommendedUser (prefs,user,n*2,similarity)

     #2.基于物品
     cs = calculateSimilarItems(prefs,n*2,similarity)#物品相似度的离线字典：{'电影1'：[(0.3,'电影2')，...],...}
     ranking_item = getRecommendedItems(prefs,cs,user,n*2)

     #3.评分预测：物品取交集，值取平均数
     for item1 in ranking_user:
          for item2 in ranking_item:
               if item1[1] == item2[1]:
                    rankings += [((item1[0]+item2[0])/2,item[1])]

     #4.top_n推荐
     rankings.sort()
     rankings.reverse()
     return rankings[0:n]



#平均评分(打分尺度)
def means(prefs,user):
     Ra = 0
     i = 0
     for p in prefs[user]:
          Ra += prefs[user][p]
          i = i + 1
     Ra = Ra/i
     return Ra    


#itemMatch:基于物品的离线字典，提前算好，以后直接加载
itemMatch_sp = {}

#5.推荐2:评分预测用论文介绍的方法（理论上更精确）
#prefs:用户-物品矩阵
#itemMatch:物品相似度字典，提前计算好直接调用---重写的方法主要卡在计算上（我写的对吗？）
def spCF2(prefs,itemMatch_sp,user,n=30,similarity=simTrans):

     rankings = []

     #1.基于用户
     totals={}
     simSums={}
            
     for other in prefs:
          if other==user: continue
          sim=similarity(prefs,user,other)
          if sim<=0: continue

          for item in prefs[other]:
               if item not in prefs[user] or prefs[user][item]==0:
                    totals.setdefault(item,0)
                    totals[item] += (means(prefs,user) + (prefs[other][item] - means(prefs,other))*sim)#本文第二亮点：y评分预测的最终计算方式
                    simSums.setdefault(item,0)
                    simSums[item]+=sim
                    
          ranking_user = [(total/simSums[item],item) for item,total in totals.items()]

     print len(ranking_user)
     
     #2.基于物品
     ranking_item = getRecommendedItems(prefs,itemMatch,user,1000)#1000:结果不受限

     #3.评分预测：物品取交集，值取平均数
     for item1 in ranking_user:
          for item2 in ranking_item:
               if item1[1] == item2[1]:
                    rankings += [((item1[0]+item2[0])/2,item[1])]
     print len(rankings)
     
     #4.top_n推荐
     rankings.sort()
     rankings.reverse()
     return rankings[0:n]



#基于用户
def SPCF3(prefs,person,n=30,similarity=simTrans):

    rankings = getRecommendedUser (prefs,person,n,similarity)
    
    return rankings


#测试
if __name__ == "__main__":

     '''
     m = loadMovieLens()

     r = spCF3(m,'96',20)
     print len(r)
     #print r
     
     mm = calculateSimilarItems(m,1,simTrans)
     print len(mm)
     print mm
     '''

     a,b = loaddata()
     r = spCF3(a,'9856',12)
     print r
     

     
