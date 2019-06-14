# -*- coding: UTF-8 -*-

from __future__ import division
#from data import *
from data import critics
from data import loadMovieLens
from math import sqrt


################
#常用相似度函数
#采用5个基本测量函数
#注意:相似度测量即比较两者差异，数值越大相似度越高
#基于用户:数据集+两人(两人都评分的物品的评分差异)
#基于物品:数据集+两物(两物都被评分的用户的评分差异)
################


#1.欧几里得距离
def sim_distance(prefs,person1,person2):
    si={}#共同评分的物品集合
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    #没有共同之处=0
    if len(si)==0:
        return 0
    #所有差值的平方和
    sum_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                     for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sqrt(sum_squares))


#2.皮尔逊相关系数
def sim_pearson(prefs,p1,p2):
    si={}#共同集合
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    #si={'Lady in the Water': 1, 'Snakes on a Plane': 1, 'Just My Luck': 1, 'Superman Returns': 1, 'You, Me and Dupree': 1, 'The Night Listener': 1}
    #共同集合个数
    n=len(si)
    #没有共同之处=1
    if n==0: return 1
    #对所有偏好求和
    sum1=sum(prefs[p1][it] for it in si)#x1+x2+...+x6
    sum2=sum(prefs[p2][it] for it in si)#y1+y2+...+y6
    #求平方和
    sum1sq=sum([pow(prefs[p1][it],2) for it in si])#x1²+x2²+...+x6²
    sum2sq=sum([pow(prefs[p2][it],2) for it in si])#y1²+y2²+...+y6²
    #求乘积之和
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])#(x1*y1+x2*y2+...+x6*y6)
    #计算皮尔逊值
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1sq-pow(sum1,2)/n) * (sum2sq-pow(sum2,2)/n))
    if den==0: return 0
    r=num/den
    return r

#######度量方法以欧几里得距离和皮尔逊相关系数为主

#3.余弦相似度
def sim_cosine(item_tags,i,j):
    ret = 0
    for b,wib in item_tags[i].items():
        if b in item_tags[j]:
            ret +=wib*item_tags[j][b]
    ni = 0
    nj = 0
    for b,w in item_tags[i].items():
        ni +=w*w
    for b,w in item_tags[j].items():
        nj +=w*w
    if ret == 0:
        return 0
    return ret/math.sqrt(ni*nj)


#4.曼哈顿距离
def sim_manhatan(p,q):
    #计算两者共有
    same = 0
    for i in p:
        if i in q:
            if i in q:
                same +=1
    #计算曼哈顿
    n = same
    vals = range(n)
    distance = sum(abs(p[i] - q[i]) for i in vals)
    return distance


#5.jaccard系数
#当数据集是二元变量时(0或1)
def sim_jaccard(p,q):
    c = [a for i in p if v in b]
    return float(len(c))/(len(b)-len(b))



#测试
if __name__ == "__main__":
    print('欧几里得方法:')
    print(sim_distance(critics,'Lisa Rose','Gene Seymour'))

    print('皮尔逊方法:')
    print(sim_pearson(critics,'Lisa Rose','Gene Seymour'))


    
    
