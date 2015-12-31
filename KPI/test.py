# coding = utf-8
'''
Created on Oct 23, 2015

@author: Administrator
'''


import numpy as np  
import queue

from _random import Random
from numpy import arange
path='C:/Users\Administrator\Desktop'
import random
import matplotlib.pyplot as plt
import xlrd
import xlwt
import math
import time 
import queue


def GetEntropyAndSplitPoint(feature, labels):
    entropyDic = {}
    minEntropy = 1
    minEntropySplit = 0
    for splitPoint in feature:
        if(splitPoint in entropyDic.keys()):
            continue
        else:
            entropy = EntropyCalculation(feature, labels, splitPoint)
            if(entropy<minEntropy):
                minEntropy = entropy
                minEntropySplit = splitPoint
            entropyDic[splitPoint] = entropy
    return minEntropy,minEntropySplit
    
def EntropyCalculation(feature,labels,splitPoint):
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
    
    return entropy
  
    
def test():
    data = xlrd.open_workbook('C:/Users\Administrator\Desktop\subset.xls')    
    sheet = data.sheet_by_index(0) 
    
    x = []
    y = []
    for index,item in enumerate(sheet.col_values(10)[2:]):
        y.append(item)
        x.append(sheet.cell_value(index+2,9))
    plt.figure()
    plt.plot(x,y,"*")
    plt.show()
    
    
    
def dataPreProcessing():
    data = xlrd.open_workbook(path+"\data.xls")
    sheetInput = data.sheets()[0]      
    workbook = xlwt.Workbook()
    sheetOutput = workbook.add_sheet('test')
    rowWrite = 0
    PosRatio = 1/3
    for row in range(2):
        data = [sheetInput.cell_value(row, col) for col in range(sheetInput.ncols)] 
        for col, value in enumerate(data):
            sheetOutput.write(rowWrite, col, value)
        rowWrite += 1
    
    for row in range(2,sheetInput.nrows):
        data = [sheetInput.cell_value(row, col) for col in range(sheetInput.ncols)]
        if(data[-2]=="NIL"):
            continue
        elif(data[-2]==100):
            if(random.random()>PosRatio):
                continue
            
        elif(data[-2]>=99.5):
            continue
        NoNIL = True
        for item in data:
            if(item=="NIL"):
                NoNIL = False
        if(not NoNIL):
            continue
        for col, value in enumerate(data):
            sheetOutput.write(rowWrite, col, value)
        rowWrite += 1
 
    workbook.save('C:/Users\Administrator\Desktop\subset.xls')
    
    '''
    statistics = [0,0,0]
    count = 0
    data_split = 99
    num_bins = 50
    for title in range(8,9):
        x = []
        y = []
         
        TestCol = table.col_values(title)
        for index in range(2,len(RRCSuccessfulBuiltRatio)):
            if(RRCSuccessfulBuiltRatio[index]!="NIL" and AvgUpstreamCode[index]!="NIL"):
                if(RRCSuccessfulBuiltRatio[index]>data_split and random.random()<0.1):
                    continue
                x.append(TestCol[index])
                y.append(RRCSuccessfulBuiltRatio[index])
      
        plt.figure()
        plt.hist(x, num_bins, normed=1, facecolor='green', alpha=1)
        plt.xlabel(title)
        plt.ylabel("RRCSuccessfulBuiltRatio")
        #plt.plot(x,y,"*")
    plt.show()
    '''

 

if __name__=="__main__":
    path = "C:\\Users\Administrator\Desktop"
    fileName = "\\zhu.xlsx"
    sheet = xlrd.open_workbook(path+fileName).sheet_by_index(0)
    print(sheet.col_values(0))
    print(sheet.col_values(1))
    book = xlwt.Workbook()
    sheetO = book.add_sheet("test")
    for index in range(sheet.nrows):
        sheetO.write(index,0,sheet.cell_value(index,0))
        if(sheet.cell_value(index,1)==1):
            sheetO.write(index,1,"男")
        else:
            sheetO.write(index,1,"女")
    book.save(path+"\gather.xls")
    
    
    
    
    