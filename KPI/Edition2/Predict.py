# -*- coding=utf-8 -*-
''' 
@author: YANG
'''

import pickle 
from Edition2.FileInput import FileInput
import os
from Edition2.Train import Train

class Predict():
    '''

	给定一组异常数据，给出异常数据对应的根因及其各个根因所占相对、绝对权重

	# 具体的根因应该由决策树的结构及给定的某一item各个特征决定；
	# 权重，在2.0版本中利用信息熵增益来确定。
    '''
    def __init__(self):
        '''
        tree = {Position:[selectedAttr, splitPoint, entropy]}
        # position 是各个节点在决策树中所处的位置， 根节点处于位置 “1”
        # selectedAttr 表示该节点选取的属性，以特征下标表示，而非名称
        # splitPoint 表示以selectedAttr为判别属性时，分界属性值是什么
        # entropy表明在该节点处所有统计数据的熵情况
        '''
        
        reader = open(os.getcwd()+"\model","rb")
        self.tree = pickle.load(reader)
        reader.close()

    '''
    cellId in 1.xls
    3 206 0.01456 132180_Ang_Mo_Kio_St_31_Blk_319
    8 412 0.01942 142560_Ang_Mo_Kio_St_22_Blk_207
    5 412 0.01214 146150_Bishan_St_23_Blk_288
    2 206 0.00971 144760_Sin_Ming_Autocare
    5 206 0.02427 130760_Ang_Mo_Kio_Ave_10_Blk_405
    45 412 0.10922 146680_Ang_Mo_Kio_Ave_1_Blk_331 

    '''
    def Predict(self):
        features, labels = FileInput().InputForPredict(fileName="1", rowBegin=8, cols=Train().DefineCols(label=17, \
            filteredCols=[i for i in range(4)]+[27,28,29,30]), cellId = "146680_Ang_Mo_Kio_Ave_1_Blk_331")
        print(features.shape) 


        RootCause = {}
        for feature in features:
            path = self.findPath(feature)
            for index in range(len(path)-1):
                try:
                    RootCause[path[index][0]] += (path[index][2][0]-path[index+1][2][0])
                except:
                    try:
                        RootCause[path[index][0]] = (path[index][2][0]-path[index+1][2][0])
                    except:
                        print(path[index],path[index+1])

        dic = FileInput().InputGetDic(fileName="1", cols=Train().DefineCols(label=17, filteredCols=[i for i in range(4)]+[27,28,29,30]))
        l = sorted(RootCause.items(), key=lambda x:x[1], reverse = True)
        for item in l:
            try:
                print(item[0])
            except Exception as e:
                print(e)
        return
        for item in dic:
            print(item, dic[item])

    def findPath(self, feature):
        '''
    	记录每条item在决策树中游走的过程，记录经过的节点，及各个节点的特性
    	'''
        path = []
        position = 1
        node = self.tree[position]
        path.append(node)
        while(node[0]!=-1):
            if(feature[node[0]]<node[1]):
                position *= 2
            else:
                position *= 2
                position += 1
            node = self.tree[position]
            path.append(node)
        return path


    def VisualizeTree(self):
        i = 1
        height = 0
        while(height<10):
            while(i<2**height):
                if(self.tree.__contains__(i)):
                    print(str(self.tree[i][0])+" ", end="")
                else:
                    print(" ", end="")
                i += 1
            print()
            height += 1


import math
if __name__=="__main__":
    obj = Predict()
    print(len(obj.tree))
    #VisualizeTree(obj.tree)
    obj.Predict()








