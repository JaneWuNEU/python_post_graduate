# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:39:55 2016

@author: User
"""
import queue
q = queue.Queue()
print(q.empty())
q.put(1)
q.put(2)
print(q.qsize(),int(q.get()),q.qsize())
'''
temp = int(q.get())
print(temp)
print(q)
'''