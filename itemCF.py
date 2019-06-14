# -*- coding: UTF-8

from __future__ import division
from data import *
from data2 import *
from similarity import *
from math import sqrt

#基于物品的推荐
#1.计算离线字典，{'电影1'：[(0.3,'相似电影')...]...}
#2.基于物品，依据用户已看的电影，结合离线字典，给出相关推荐



#寻找相似邻居：相似用户和相似物品都可以通过本函数
def topMatches(prefs,person,n=10,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other)
            for other in prefs if other!=person]#当前用户与其他用户的相似度集合
   
    #降序排序
    scores.sort()#升序
    scores.reverse()#降序
    return scores[0:n]#取两者相似度靠前的前n位


#1.离线字典
#注:1.提前计算，使用时直接加载
#2.本函数应该频繁执行，保证相似度不会过期
#3.当用户和物品基数较大后，字典评价值趋于稳定
#n:控制每个物品的相似邻居的个数（降序）
def calculateSimilarItems(prefs,n=10,similarity=sim_distance):
    
    result={}#相似物品集合
    
    itemPrefs=transformPrefs(prefs)#对原始的偏好矩阵倒置处理---以物品为中心
    
    c=0
    for item in itemPrefs:
        c+=1#更新状态变量
        if c%100==0: print("%d / %d" % (c,len(itemPrefs)))
        
        #寻找相似物品
        scores=topMatches(itemPrefs,item,n=n,similarity=similarity)#最相近的邻居
        result[item]=scores

    return result#{'电影1'：[(0.3,'电影2'),(0.3,'电影3'),...],'电影2'：[(0.3,'相似电影'),(0.3,'相似电影'),...],...}


#2.基于物品的推荐
#注;itemMatch:提前计算，使用时直接加载
def getRecommendedItems(prefs,itemMatch,user,n):
    
    userRatings=prefs[user]
    scores={}
    totalSim={}
    
    #1.遍历当前用户评分的物品
    for (item,rating) in userRatings.items():#1.基于物品
        
        #遍历与当前物品相似的物品
        for (similarity,item2) in itemMatch[item]:#两物品相似度---离线计算+调结果
            
            #忽略当前用户已评价物品
            if item2 in userRatings: continue
            
            #评价值与相似度的加权之和
            scores.setdefault(item2,0)
            scores[item2]+=rating*similarity#2.待推荐用户对该物品的评分*两物品的相似度（离线：计算后调结果，趋于稳定）
            
            #全部相似度之和
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
            
    #2.将每个合计值除以加权之和，求出平均值
    rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

    #3.排序
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]



#测试
if __name__ == "__main__":

    '''
    m=loadMovieLens()
    c=calculateSimilarItems(m,50)
    r=getRecommendedItems(m,c,'87',30)
    print len(c)
    print len(r)
    print r
    '''

    a,b = loaddata()
    s =  calculateSimilarItems(a,12)
    r = getRecommendedItems(a,s,'9856',12)
    print r
    
