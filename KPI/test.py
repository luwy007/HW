# coding = utf-8
'''
Created on Oct 23, 2015

@author: Administrator
'''
from Edition2.Train import Train
from Edition2.Predict import Predict
import time
import numpy as np
import xlrd

'''
    cellId in 1.xls
    3 206 0.01456 132180_Ang_Mo_Kio_St_31_Blk_319
    8 412 0.01942 142560_Ang_Mo_Kio_St_22_Blk_207
    5 412 0.01214 146150_Bishan_St_23_Blk_288
    2 206 0.00971 144760_Sin_Ming_Autocare
    5 206 0.02427 130760_Ang_Mo_Kio_Ave_10_Blk_405
    45 412 0.10922 146680_Ang_Mo_Kio_Ave_1_Blk_331 

'''



if __name__=="__main__": 

    



    cellIds = ["132180_Ang_Mo_Kio_St_31_Blk_319",\
               "142560_Ang_Mo_Kio_St_22_Blk_207",\
               "146150_Bishan_St_23_Blk_288",\
               "144760_Sin_Ming_Autocare",\
               "130760_Ang_Mo_Kio_Ave_10_Blk_405",\
               "146680_Ang_Mo_Kio_Ave_1_Blk_331"] 
    fileName = "1"
    sheet = xlrd.open_workbook("c:\\users\yang\desktop\data\\%s.xls"%(fileName)).sheet_by_index(0)
    

    for cellId in cellIds[:]:
        count = 0
        NEG = 0
        for rowIndex in range(8,sheet.nrows):
            if(sheet.cell_value(rowIndex,2)!=cellId):
                continue
            if(sheet.cell_value(rowIndex,17)<=99.5):
                #print(cellId,sheet.cell_value(rowIndex,3), sheet.cell_value(rowIndex,0),sheet.cell_value(rowIndex,17))
                NEG += 1
            count += 1
        print(cellId, NEG, count, NEG/count)
    

  
    






