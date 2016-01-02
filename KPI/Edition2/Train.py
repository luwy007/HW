'''
Created on 2015/12/31

@author: YANG
'''

from Edition2.FileInput import FileInput
import math

class Train():
    class Node():
        def __init__(self):
            self.attrIndexSelected = -1      # -1 represents selecting no feature
            self.SubNodes = []               # contains left and right son
            self.SplitPoint = 0              # left son <, right son >=
            self.Label = 0                   # 0 represents the node is not leaf node
            self.dataNum = 0                 # the number of data which should be classified by this node
            self.Position = -1               # the position of root is 1
    
    def train(self, path, fileName):
        
        features, labels = FileInput.Input(path, fileName)
        tree = self.TreeGrowth(features, labels)
        
    def TreeGrowth(self, features, labels):
        tree = self.Node()
        return tree
     
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


















