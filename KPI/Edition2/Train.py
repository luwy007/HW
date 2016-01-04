# -*- coding=utf-8 -*-
'''
@author: YANG
'''

from Edition2.FileInput import FileInput
import math
import pickle
import os

ENTROPYLIMIT = 0.5


class Train():
    '''
    这个Node的定义是之前版本的遗留物，留在这里当做启发

    '''
    class Node():
        def __init__(self):
            self.attrIndexSelected = -1      # -1 represents selecting no feature
            self.SubNodes = []               # contains left and right son
            self.SplitPoint = 0              # left son <, right son >=
            self.Label = 0                   # 0 represents the node is not leaf node
            self.dataNum = 0                 # the number of data which should be classified by this node
            self.Position = -1               # the position of root is 1

    def __init__(self):
        '''
        tree = {Position:[selectedAttr, splitPoint, entropy]}
        # Position 是各个节点在决策树中所处的位置， 根节点处于位置 “1”
        # selectedAttr 表示该节点选取的属性，以特征下标表示，而非名称
        # splitPoint 表示以selectedAttr为判别属性时，分界属性值是什么
        # entropy表明在该节点处所有统计数据的熵情况
        '''
        self.tree = {}
 
    def Train(self, path, fileName):
        features, labels = FileInput.Input(path, fileName)
        self.TreeGrowth(features, labels)
          
    def BuildTree(self, features, labels):
        filteredFea = [0]*len(features[0])
        filteredSam = [0]*len(labels)
        # ChooseBestAttr返回的第一个参数是三元tuple，注意！
        rootEntropy, rootAttr, rootSplitPoint = self.ChooseBestAttr(features,labels,filteredFea,filteredSam)
        self.tree[1] = [rootAttr, rootSplitPoint, rootEntropy]
        filteredFea[rootAttr] = 1
        isLeaf = False
        if(rootEntropy[1]<ENTROPYLIMIT):
            isLeaf = True
        self.TreeGrowth(features, labels, filteredFea, filteredSam, 1, True, isLeaf)
        
        if(rootEntropy[2]<ENTROPYLIMIT):
            isLeaf = True
        self.TreeGrowth(features, labels, filteredFea, filteredSam, 1, False, isLeaf)
 
        writer = open(os.getcwd()+'\model','w')
        pickle.dump(self.tree, writer)
        writer.close()
  
    def TreeGrowth(self, features, labels, filteredFea, filteredSam, parentPosition, isLeft, isLeaf):
        '''
        如果是计算父节点时发现此节点不添加任何判断属性，熵就已经达标的话，便将此节点定义为叶节点
        '''
        if(isLeaf): 
            if(isLeft):
                entropy = [self.tree[parentPosition][0][1],-1,-1]
                self.tree[2*parentPosition] = [-1, -1, entropy]
            else:
                entropy = [self.tree[parentPosition][0][2],-1,-1]
                self.tree[2*parentPosition+1] = [-1, -1, entropy]
            return



        parentSelectedAttr = self.tree[parentPosition][0]
        parentSplitPoint = self.tree[parentPosition][1]
        
        if(isLeft):
            leftFilteredSam = filteredSam[:]
            leftFilteredFea = filteredFea[:]
            for i in range(len(labels)):
                if(features[i][parentSelectedAttr]>=parentSplitPoint):
                    leftFilteredSam[i] = 1

            entropy, attr, splitPoint = self.ChooseBestAttr(features,labels,filteredFea,leftFilteredSam)   
            self.tree[2*parentPosition] = [attr, splitPoint, entropy]
            leftFilteredFea[attr] = 1
            self.TreeGrowth(features, labels, leftFilteredFea, leftFilteredSam, 2*parentPosition, True, entropy[1]<ENTROPYLIMIT)
            self.TreeGrowth(features, labels, leftFilteredFea, leftFilteredSam, 2*parentPosition, False, entropy[2]<ENTROPYLIMIT)
        else:
            rightFilteredSam = filteredSam[:]
            rightFilteredFea = filteredFea[:]
            for i in range(len(labels)):
                if(features[i][parentSelectedAttr]<parentSplitPoint):
                    rightFilteredSam[i] = 1

            entropy, attr, splitPoint = self.ChooseBestAttr(features,labels,filteredFea,rightFilteredSam)   
            self.tree[2*parentPosition+1] = [attr, splitPoint, entropy]
            rightFilteredFea[attr] = 1
            self.TreeGrowth(features, labels, rightFilteredFea, rightFilteredSam, 2*parentPosition+1, True, entropy[1]<ENTROPYLIMIT)
            self.TreeGrowth(features, labels, rightFilteredFea, rightFilteredSam, 2*parentPosition+1, False, entropy[2]<ENTROPYLIMIT)

        return
 
    def ChooseBestAttr(self, features, labels, filteredFea, filteredSam):
        '''
        features contains several features, labels contains +1 or -1, 
        selected represents whether the feature selected, 0 not selected, 1 selected
        filteredFea 1表示已经在之前的节点中选过了
        filteredSam 1表示已经在之前的节点中被过滤掉了
        '''
        MinEntropy = [1,0,0]
        MinEntropyIndex = -1
        MinEntropySplitPoint = -1
        
        for i in range(len(filteredFea)):
            if(filteredFea[i]==1):
                continue
            tempData = []
            tempLabels = []
            for index in range(len(filteredSam)):
                if(filteredSam[index]==1):
                    continue
                tempData.append(features[index][i])
                tempLabels.append(labels[index])
            Entropy,SplitPoint = self.GetEntropyAndSplitPoint(tempData, tempLabels)
            if(Entropy[0]<=MinEntropy[0]):
                MinEntropy = Entropy
                MinEntropyIndex = i
                MinEntropySplitPoint = SplitPoint
                
        return MinEntropy, MinEntropyIndex, MinEntropySplitPoint

    def GetEntropyAndSplitPoint(self, feature, labels):
        #feature is a 1-dimension vector, |feature|=|labels|,labels contains +1 or -1
        entropyDic = {}
        minEntropy = [1,0,0]
        minEntropySplit = 0
        
        for splitPoint in feature:
            if(splitPoint in entropyDic.keys()):
                continue
            else:
                entropy = self.EntropyCalculation(feature, labels, splitPoint)
                if(entropy[0]<minEntropy[0]):
                    minEntropy = entropy
                    minEntropySplit = splitPoint
                entropyDic[splitPoint] = entropy
        
        return minEntropy,minEntropySplit
        
    def EntropyCalculation(self,feature,labels,splitPoint):
        #feature is a 1-dimension vector, |feature|=|labels|, splitPoint is the boundary in feature
        if(len(labels)==0):
            print("entropy calculation error! feature has no elements")
            return -1
        
        YPosXLarger = 0
        YPosXSmaller = 0
        YNegXLarger = 0
        YNegXSmaller = 0 
        
        for index,item in enumerate(feature):
            if(labels[index]==1):
                if(item>=splitPoint):
                    YPosXLarger += 1
                else:
                    YPosXSmaller += 1
            else:
                if(item>=splitPoint):
                    YNegXLarger += 1
                else:
                    YNegXSmaller += 1
        
        LargerSum = YPosXLarger+YNegXLarger
        SmallerSum = YPosXSmaller+YNegXSmaller
        LargerEntropy = 0
        SmallerEntropy = 0
        
        if(LargerSum==0):
            pass
        else:
            if(YPosXLarger==0):
                pass
            else:
                p = YPosXLarger/LargerSum
                LargerEntropy -= p*math.log2(p)
            
            if(YNegXLarger==0):
                pass
            else:
                p = YNegXLarger/LargerSum
                LargerEntropy -= p*math.log2(p)
        
        if(SmallerSum==0):
            pass
        else:
            if(YPosXSmaller==0):
                pass
            else:
                p = YPosXSmaller/SmallerSum
                SmallerEntropy -= p*math.log2(p)
            
            if(YNegXSmaller==0):
                pass
            else:
                p = YNegXSmaller/SmallerSum
                SmallerEntropy -= p*math.log2(p)

        entropy = (LargerSum/(LargerSum+SmallerSum))*LargerEntropy+\
                  (SmallerSum/(LargerSum+SmallerSum))*SmallerEntropy
        
        return entropy, SmallerEntropy, LargerEntropy


    def Pruning(self):
        pass













