


'''
Created on Nov 5, 2015

@author: Administrator
'''
#_*_ coding:UTF-8 _*_ 


import math
import numpy as np
import xlrd
import time
import queue




path='C:/Users\yang\Desktop'

class Node:
    def __init__(self):
        self.attrIndexSelected = -1      # -1 represents selecting no feature
        self.SubNodes = []               # contains left and right son
        self.SplitPoint = 0              # left son <, right son >=
        self.Label = 0                   # 0 represents the node is not leaf node
        self.dataNum = 0                 # the number of data which should be classified by this node
        self.Position = -1               # the position of root is 1
        
class DT:
    def __init__(self):
        self.root = Node()
        self.node_num = 0
        self.leafNodes = {}
        
    def BuildTree(self,data,labels):
        '''
        data contains n*34 samples, labels contains n +1 or -1
        '''
        #print(self.node_num, time.strftime('%H:%M:%S',time.localtime(time.time())))
        filteredSam = [0]*data.shape[0]
        filteredFea = [0]*data.shape[1]
        # filteredSet contains the indexes of those self-defined filtered feature in advance
        filteredFeaSet = [0,1,2,3,4,5,6,10,11,12,13,14,15,16,17,18,19,20,21]
        for i in filteredFeaSet:
            filteredFea[i] = 1
        
        entropy, self.root.attrIndexSelected, self.root.SplitPoint = self.ChooseBestAttr(data, labels, filteredFea, filteredSam)
        filteredFea[self.root.attrIndexSelected] = 1
        self.root.dataNum = len(filteredSam)-sum(filteredSam)
        self.root.Position = 1
        if(entropy[0]<0.5):
            return 
        #print(1,entropy,self.root.attrIndexSelected)
        self.TreeGrowth(data, labels, filteredFea, self.root, filteredSam,1,entropy)
    
    def TreeGrowth(self,data,labels,filteredFea,node,filteredSam,position,NodeEntropy):
        
        if(self.SelectedAll(filteredFea)):
            return
        
        StopPoint = 0.5 
        
        # left node growth
        leftSon = Node()
        leftFilteredSam = filteredSam[:]
        self.FilterDataFromFatherNode(data, node.attrIndexSelected, node.SplitPoint, True, leftFilteredSam)
        leftSon.dataNum = len(leftFilteredSam)-sum(leftFilteredSam)
        leftSon.Position = 2*position
        node.SubNodes.append(leftSon)
        if(NodeEntropy[2]<StopPoint): 
            #print("leaf node derived by "+str(node.attrIndexSelected))
            try:
                self.leafNodes[node.attrIndexSelected] += (len(leftFilteredSam)-sum(leftFilteredSam))
            except:
                self.leafNodes[node.attrIndexSelected] = (len(leftFilteredSam)-sum(leftFilteredSam))
            
            return
        else:  
            leftFilteredFea = filteredFea[:]
            entropy,leftSon.attrIndexSelected,leftSon.SplitPoint = self.ChooseBestAttr(data, labels, leftFilteredFea,leftFilteredSam)
            #print(2*position,entropy,leftSon.attrIndexSelected)
            #print(time.strftime('%H:%M:%S',time.localtime(time.time())))
             
            leftFilteredFea[leftSon.attrIndexSelected] = 1
            self.TreeGrowth(data, labels, leftFilteredFea, leftSon, leftFilteredSam,2*position,entropy)
        
        
        # right node growth
        rightSon = Node()
        rightFilteredSam = filteredSam[:]
        self.FilterDataFromFatherNode(data, node.attrIndexSelected, node.SplitPoint, False, rightFilteredSam)
        rightSon.dataNum = len(rightFilteredSam)-sum(rightFilteredSam)
        rightSon.Position = 2*position+1
        node.SubNodes.append(rightSon)
        if(NodeEntropy[1]<StopPoint):
            #print("leaf node derived by "+str(node.attrIndexSelected))
            try:
                self.leafNodes[node.attrIndexSelected] += (len(rightFilteredSam)-sum(rightFilteredSam))
            except:
                self.leafNodes[node.attrIndexSelected] = (len(rightFilteredSam)-sum(rightFilteredSam))
                
            
            return
        else: 
            
            rightFilteredFea = filteredFea[:]
            entropy,rightSon.attrIndexSelected,rightSon.SplitPoint = self.ChooseBestAttr(data, labels, rightFilteredFea,rightFilteredSam)
            #print(2*position+1,entropy,rightSon.attrIndexSelected)
            #print(time.strftime('%H:%M:%S',time.localtime(time.time())))
            rightFilteredFea[rightSon.attrIndexSelected] = 1
            self.TreeGrowth(data, labels, rightFilteredFea, rightSon, rightFilteredSam,2*position+1,entropy)
           
    def SelectedAll(self,selected):
        sum = 0
        for item in selected:
            sum += item
        if(sum==len(selected)):
            return True
        return False
    
    def FilterDataFromFatherNode(self,data,splitIndex,splitPoint,isLeftSon,filteredSam):
        '''
        update filteredSam
        '''
        if(isLeftSon):
            for index,item in enumerate(filteredSam):
                if(item==1):
                    continue
                if(data[index][splitIndex]>=splitPoint):
                    #filter those samples which should be trained by right subTree
                    filteredSam[index] = 1
        else:
            for index,item in enumerate(filteredSam):
                if(item==1):
                    continue
                if(data[index][splitIndex]<splitPoint):
                    filteredSam[index] = 1
 
    def ChooseBestAttr(self, data, labels, filteredFea, filteredSam):
        '''
        data contains several features, labels contains +1 or -1, 
        selected represents whether the feature selected, 0 not selected, 1 selected
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
                tempData.append(data[index][i])
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
        
        return entropy,LargerEntropy,SmallerEntropy

    def OutputTree(self):
        q = queue.Queue()
        q.put(self.root)
        changeLine = [1]
        while q.qsize():
            node = q.get()
            for subNode in node.SubNodes:
                q.put(subNode)
            self.OutputNode(node,changeLine)

    def OutputNode(self,node,changeLine):
        if(changeLine[0]<=node.Position):
            changeLine[0] *= 2
            print("\n", end="")
        else:
            print("\t\t", end="")
        
        if(node.attrIndexSelected!=-1):
            print('  P: '+str(node.Position)+' A: '+str(node.attrIndexSelected)+' S: '+str(node.dataNum)+' SP: '+str(node.SplitPoint)+'  ', end='')
        else:
            print('{ P: '+str(node.Position)+' A: '+str(node.attrIndexSelected)+' S: '+str(node.dataNum)+' SP: '+str(node.SplitPoint)+' }', end='')
             
 
class FileInput:
    def getDataAndLabels(self):
        book = xlrd.open_workbook(path+"\subset.xls")
        sheet = book.sheet_by_index(0)
        
        data = []
        for rowIndex in range(2,sheet.nrows):
            temp = []
            for colIndex in range(1,35):
                temp.append(sheet.cell_value(rowIndex,colIndex))
            data.append(temp)
        data = np.array(data)
        
        labels = []
        for item in sheet.col_values(35)[2:]:
            if(item>99.5):
                labels.append(1)
            else:
                labels.append(-1)
        
        return data,labels

 


if __name__=="__main__":  
    data,labels = FileInput().getDataAndLabels()
    tree = DT()
    tree.BuildTree(data,labels) 
    tree.OutputTree()
    print()
    print(tree.leafNodes) 
    





