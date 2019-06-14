# -*- coding: UTF-8 -*-

from __future__ import division
from data import *
from data2 import *
from similarity import *
from itemCF import *
import datetime
import time

#用户兴趣变化部分的实现

#基于时间调数据权重
#参数: u-用户 i-指定资源 a=权重增长指数∈【0,1】
#注意：时间数据为对电影的评分时间，即默认为访问时间=评分时间
def getWT(prefer,u,i,a=0.5):
    
    Du=0#时间间隔=用户最早访问与i的访问时间(反映资源的实时性)
    Lu=0#用户访问时长=最早访问与最晚访问
    time=[]#以列表返回用户u的访问时间
    
    #计算相关时间参数
    t=prefer.get(u).values()#用户u的访问时间
    time=list(t)
    earlyTime=time[0]#最早访问时间
    
    lateTime=time[0]#最晚访问时间
    for t in time:
        if t<=earlyTime:
            earlyTime=t
        if t>=lateTime:
            lateTime=t
    ITime=prefer.get(u).get(i)#获取指定资源访问时间
    
    #计算Du和Lu
    Du=ITime-earlyTime
    Lu=lateTime-earlyTime
    
    #计算基于时间的数据权重
    WT=(1-a)+a*(Du/Lu)
    return WT


#基于资源相似度的数据权重
#参数: u-用户
#i-指定资源
#时间窗T(/天)：用户最近T时间段访问资源（注:因为movielens电影都是70年代的，暂设T为22年，1998~2019）
def getWS(prefer,u,i,T=10):
    
    Iut={}#用户u近期访问资源集合
    
    #当前时间的时间戳
    currentTime=time.time()
    #T天以前的时间戳
    timeBeforeT=currentTime-T*(60*60*24)#时间戳将时间换算为秒，(60*60*24)=1天
  
    
    #获取近期资源集合Iut
    #思路:1.近期资源名称列表 2.加载用户-物品评分字典 3.生成u近期访问资源的评分字典
    keys=[]#以列表形式确定u近期访问的资源名称
    for key,values in prefer.get(u).items():
        if values<=currentTime and values>=timeBeforeT:
            keys.append(key)
    Iut=prefer.get(u)#加载用户u的评分字典
    for key,values in Iut.items():
        if key not in keys: 
            del Iut[key]#保留时间窗T下用户u的访问资源
 
    #获取Iut的资源数目
    size=len(Iut)
    #print 'size'
    #print size
    #计算Iut内i和其它资源的相似度之和
    simSums=sum([pow(Iut[i]-Iut[j],2) for j in Iut if j !=i])
    sim_distance=1/(1+sqrt(simSums))#使用欧几里得测量函数
    
    #计算基于资源相似度的数据权重权重
    if size==0:WS=0
    else: WS=sim_distance/size
    
    return WS


#两种数据权重的结合
#参数: WT-基于时间调数据权重 WS-基于资源相似度的数据权重 x=比例因子∈【0,1】
def getWTS(prefer,u,i,x=0.6):
   
    #将两种权重进行线性加权
    WT=getWT(prefer,u,i)
    WS=getWS(prefer,u,i)
    WTS=x*WT+(1-x)*WS
    return WTS#返回同时基于时间和资源相似度的权重函数值


#生成推荐
#n-结果个数
def TIMECF(prefs_rating,prefs_time,user,n=20,sim=sim_distance):

    #已访问物品集合
    Iu = []
    for u in prefs_rating[user]:
        Iu.append(u)
    #print '已访问资源总数len(Iu)'
    #print len(Iu)

    #候选推荐集---控制每个Iu的邻居的个数，推荐集个数控制好  
    itemMatch = calculateSimilarItems(prefs_rating,3)#资源近邻模型M：物品相似度的离线字典   // 原文的K=20，此处用3，方便运行
    C = []
    for i in Iu:
        for item in itemMatch[i]:
            C.append(item[1])
    C = list(set(C))
    for j in C:
        if j in Iu:C.remove(j)
    #print '候选推荐集个数len(C)'
    #print len(C)

    #wts权重计算---只算Iu集合物品,提前算好，用时加载
    weight = {}
    for i in Iu:
        weight[i] = getWTS(prefs_time,user,i)
        
    #加权后的推荐集
    pref=transformPrefs(prefs_rating)
    rankings = []    
    for j in C:
        rec_wight = 0
        for i in Iu:
            rec_wight +=  weight[i]*sim(pref,i,j)
        rankings.append((rec_wight,j))

    #排序
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]


#测试
if __name__ == "__main__":

    '''
    movies=loadMovieLens()
    movies_time=getTime()
    
    r=getRecommendedTime2(movies,movies_time,'87',10)
    print r
    print len(r)
    '''

    a,b = loaddata()
    r = TIMECF(a,b,'9856',12)
    print r



    
     

