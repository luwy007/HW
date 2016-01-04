# -*- coding=utf-8 -*-
''' 
@author: YANG
'''

import pickle 
from Edition2.FileInput import FileInput



class Predict():
	'''

	给定一组异常数据，给出异常数据对应的根因及其各个根因所占相对、绝对权重

	# 具体的根因应该由决策树的结构及给定的某一item各个特征决定；
	# 权重，在2.0版本中利用信息熵增益来确定。


	'''
    def __init__(self):
    	'''
        tree = {Position:[selectedAttr, splitPoint, entropy]}
        # Position 是各个节点在决策树中所处的位置， 根节点处于位置 “1”
        # selectedAttr 表示该节点选取的属性，以特征下标表示，而非名称
        # splitPoint 表示以selectedAttr为判别属性时，分界属性值是什么
        # entropy表明在该节点处所有统计数据的熵情况
        '''
    	reader = open(os.getcwd()+"\model","r")
    	pickle.load(self.tree, reader)
    	reader.close()

    def Predict(self):
    	features, labels = FileInput.InputForTrain(path=os.getcwd(), fileName="1", rowBegin=8, colBegin=1, colEnd=2)
    	RootCause = {}
    	for feature in features:
    		path = self.findPath(feature)
    		for index in range(len(path)-1):
    			try:
    				RootCause[node[0]] += (path[index][2][0]-path[index+1][2][0])
    			except:
    				RootCause[node[0]] = (path[index][2][0]-path[index+1][2][0])

    	dic = FileInput.InputGetDic(path=os.getcwd(), fileName="1")
    	l = sorted(RootCause.items(), key=lambda x:x[1], reverse = True)
    	for item in l:
    		print(item,dic[item[0][0]])

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

    	return path



