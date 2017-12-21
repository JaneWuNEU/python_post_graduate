# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:48:34 2017

@author: User
"""
from sympy import *
q = Symbol("q")

c3 = Symbol("c3")
c2 = Symbol("c2")
c1 = Symbol("c1")

n1 = Symbol("n1")
n2 = Symbol("n2")
n3 = Symbol("n3")

m1 = Symbol("m1")
m2 = Symbol("m2")
m3 = Symbol("m3")

d1 = Symbol("d1")
d2 = Symbol("d2")
d3 = Symbol("d3")
d = Symbol("d")

d1=q/2*(n1-1)*n1+q*m1*n1
d2= c2*q*(n1-1)
d3= q*(n1-2)*(1-m1-c2)+q/2*(2*n1+n3-4)*(n3-1)+q*(n1+n3-2)+q*(m1+c2+m3-1)*(n1+n3-1)

print("d1=",expand(d1))
print("d2=",expand(d2))
print("d3=",expand(d3))
print("d=",expand(d1+d2+d3))
