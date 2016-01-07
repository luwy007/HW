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
    def __init__(self):
        pass


    def InputForTrain(self, path="C:\\users\yang\desktop\data", fileName="1", rowBegin=8, cols=[-2]*61):
        '''
        # path is where the training data located
        # fileName is the name of training data
        # rowBegin is the row index from where the real data stored
        # cols表示哪些列作为features，哪些作为label，哪些被抛弃，分别用0，1，-1表示。2.0版本数据总共61列
        '''
        try:
            book = xlrd.open_workbook(path+"\\"+fileName+".xls")
        except Exception as e:
            print(e)
            return 
        sheet = book.sheet_by_index(0)
        
        features = []
        for colIndex in range(len(cols)):
            if(cols[colIndex]!=0):
                continue
            temp = []
            for rowIndex in range(rowBegin,sheet.nrows):
                try:
                    temp.append(float(sheet.cell_value(rowIndex, colIndex)))
                except:
                    temp.append(0)
                    print("NIL", rowIndex, colIndex)
                    if(sheet.cell_value(rowIndex,colIndex)!="NIL"):
                        print (sheet.cell_value(rowIndex,colIndex))
            features.append(temp)
        features = np.array(features).transpose()
        
        labelIndex = -1
        for item in cols:
            labelIndex += 1
            if(item==1):
                break
        '''
        此处对正负类的划分规则，相较于工业上的阈值区分要更加严格。
        定义当指标为非完美时，便为负类，以此解决数据倾斜问题，并且可以尽可能捕捉到更多的根因识别有效信息
        '''
        labels = []
        for item in sheet.col_values(labelIndex)[rowBegin:]:
            if(item==100):
                labels.append(1)
            else:
                labels.append(-1)
        
        return features, labels



    def InputForPredict(self, path="C:\\users\yang\desktop\data", fileName="1", rowBegin=8, cols=[-2]*61, cellId=""):
        '''
        # path is where the training data located
        # fileName is the name of training data
        # rowBegin is the row index from where the real data stored
        # cols表示哪些列作为features，哪些作为label，哪些被抛弃，分别用0，1，-1表示。2.0版本数据总共61列
        '''
        try:
            book = xlrd.open_workbook(path+"\\"+fileName+".xls")
        except Exception as e:
            print(e)
            return 
        sheet = book.sheet_by_index(0)
        
        labelIndex = -1
        for item in cols:
            labelIndex += 1
            if(item==1):
                break

        labels = []
        for item in sheet.col_values(labelIndex)[rowBegin:]:
            if(item<99.5):
                labels.append(-1)
            else:
                labels.append(1)


        features = []
        for rowIndex in range(rowBegin, sheet.nrows):
            if(sheet.cell_value(rowIndex, 2)!=cellId or labels[rowIndex-rowBegin]!=-1):
                continue
            temp = []
            for colIndex in range(len(cols)):
                if(cols[colIndex]!=0):
                    continue
                temp.append(sheet.cell_value(rowIndex,colIndex))
            features.append(temp)

        return np.array(features), labels


        

    def InputGetDic(self, path="C:\\users\yang\desktop\data", fileName="1", nameRow=6, cols=[-2]*61):
        try:
            book = xlrd.open_workbook(path+"\\"+fileName+".xls")
        except Exception as e:
            print(e)
            return 
        sheet = book.sheet_by_index(0)
        dic = {}
        colIndex = 0
        for i in range(sheet.ncols):
            if(cols[i]!=0):
                continue
            dic[colIndex] = sheet.cell_value(nameRow,i)
            colIndex += 1
        return dic


if __name__=="__main__": 
    try:
        book = xlrd.open_workbook("c:\\users\yang\desktop\data\\1.xls")
        sheet = book.sheet_by_index(0)
    except Exception as e:
        print(e)


    labelIndex = 17
    cellDic = {} 
    problemCell = {}
    for index in range(8,sheet.nrows):
        try:
            cellDic[sheet.cell_value(index, 2)] += 1
        except:
            cellDic[sheet.cell_value(index, 2)] = 1
        try:
            if(sheet.cell_value(index,labelIndex)<99.5):
                try:
                    problemCell[sheet.cell_value(index,2)] += 1
                except:
                    problemCell[sheet.cell_value(index,2)] = 1
        except Exception as e:
            print(sheet.cell_value(index,labelIndex))
    l = {}
    for item in cellDic:
        try:
            print(problemCell[item], cellDic[item], round(problemCell[item]/cellDic[item],5), item)
            l[item] = round(problemCell[item]/cellDic[item],5)
        except:
            print(0, cellDic[item], round(0/cellDic[item],5), item)
            l[item] = round(0/cellDic[item],5)
    print(len(problemCell), len(cellDic))
    l = sorted(l.items(), key = lambda x:x[1], reverse=True)
    for item in l:
        print(item, cellDic[item[0]])








