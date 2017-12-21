# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 18:36:46 2016

@author: User
"""
class A:
    def __init__(self,name,age):
        self._name = name
        self._age = age

class B:
    def __init__(self,AList):
        for i in range(len(AList)):
            AList
            a = AList[i]
            print(a._name,a._age)
'''
a1 = A("Rose",24)
a2 = A("Mike",15)
Alist = list()
Alist.append(a1)
Alist.append(a2)
B(Alist)
'''
print([0,])