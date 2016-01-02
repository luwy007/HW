# _*_ coding=utf-8 _*_
'''
Created on 2015/12/31

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

    def InputForTrain(self, path, fileName, rowBegin, colBegin, colEnd):
        # path is where the training data located
        # fileName is the name of training data
        # rowBegin is the row index from where the real data stored
        # colBegin is the col index from where the data we need begins
        # colEnd is the col index at where the data we need ends
        book = xlrd.open_workbook(path+fileName+".xls")
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
 












