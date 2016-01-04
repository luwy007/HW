# -*- coding=utf-8 -*-
''' 

@author: YANG
'''

'''
for training, FileInput transform data into two parts, features and labels for train


# this part needs to be considered
for prediction, FileInput transforms data into features


'''

import xlrd
import numpy as np



class FileInput():
    '''
    给Train和Predict提供良好的数据读取接口
    针对Train，输入是文件路径名，文件名，指定的数据范围，包括哪些列是特征，哪些列是类标
    针对Predict，输入是文件路径名，文件名，指定的数据范围，包括哪些列是特征，哪些列是类标？暂不确定
    '''
    def InputForTrain(self, path="", fileName="", rowBegin=8, colBegin=1, colEnd=2):
        # path is where the training data located
        # fileName is the name of training data
        # rowBegin is the row index from where the real data stored
        try:
            book = xlrd.open_workbook(path+"\\"+fileName+".xls")
        except Exception as e:
            print(e)
            return 
        sheet = book.sheet_by_index(0)
        
        features = []
        for rowIndex in range(rowBegin,sheet.nrows):
            temp = []
            for colIndex in range(colBegin,colEnd):
                temp.append(sheet.cell_value(rowIndex,colIndex))
            features.append(temp)
        features = np.array(features)
        
        labels = []
        for item in sheet.col_values(35)[rowBegin:]:
            if(item>99.5):
                labels.append(1)
            else:
                labels.append(-1)
        
        return features, labels
 
    def InputGetDic(self, path="", fileName="", nameRow=7):
        try:
            book = xlrd.open_workbook(path+"\\"+fileName+".xls")
        except Exception as e:
            print(e)
            return 
        sheet = book.sheet_by_index(0)
        dic = {}
        for i in range(len(sheet[0])):
            dic[i] = sheet[nameRow][i]
        return dic








