# coding = utf-8
'''
Created on Oct 23, 2015

@author: Administrator
'''

import pickle
from Edition2.FileInput import FileInput


class Test():
	def __init__(self):
		self.tree = {}

	def func(self, l): 
		l[0] += 1 

import os
if __name__=="__main__":  
	RootCause = {1:2,2:3,3:-1,4:-2}
	dic = sorted(RootCause.items(), key=lambda x:x[1], reverse = True)
	print(dic)
	#help(sorted)


