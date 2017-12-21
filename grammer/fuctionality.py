# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 19:47:16 2016
Chapter 05
@author: User
"""
class Car:
    def infor(self):#self相当于java中的this，指代创建的对象本身
        print("hello world")
    def test():
        pass#2、起到了占位的作用
class House:
    price = 1000
    def __init__(self,c):
        self.color = c
        print("initil",self.color)
class A:
    def __init__(self,value1= 0,value2= 0):
        self._value1=value1
        self.__value2 = value2
    def setValue(self,value1,value2):
        self._value1 = value1
        self.__value2 = value2
    def show(self):
        print(self._value1,self.__value2)
class Fruit:
    def __init__(self):
        self.__color = "red"
        self.price = 1
class Root:
    _total = 0
    def __init__(self,v):
        self.__value = v
        Root._total+=1
    def show(self):
        print("self.__value",self.__value)
        print("Root._total",self._total)
    def __test(self,reset):
        self.__value = reset
    @classmethod
    def classShowTotal(cls):#类方法
        print(cls._total)
    @staticmethod
    def staticShow(value):
        Root._total = value
        print(Root._total) 
class Test:
    def __init__(self,value):
        self._value = value
        print(self._value)
    @property
    def _value_(self):
        return self._value
test = Test(3)
test.name = "wj"
print(test.name)
test.value = 5
print(test._value,test.value,test._value_)

'''    
car = Car()#3、创建类的对象
car.infor()
print(isinstance(car,Car))#1、用于检测该对象是否为指定类的句柄
print(isinstance(car,str))

h1 = House("red")
h2 = House("blue")
h1.name = "wj"
print(h1.price,h1.color,h1.name)
House.price =500
print(h2.price,h2.color)

a = A()
a.setValue(value1= 3,value2 = 4)
print(a._value1)
a.show()

apple = Fruit()
print(apple.price)
apple.price = 2
print(apple.price)
print(apple.price,apple._Fruit__color)
apple._Fruit__color = "blue"
print(apple.price,apple._Fruit__color)#对象属性只在该对象内有效，创建新的对象后所有值失效
peach = Fruit()
print(peach.price,peach._Fruit__color)
root = Root("jane")
root.show()
root.classShowTotal()
root.staticShow(10)
root = Root("wu")
root.show()
root.classShowTotal()
root.staticShow(11)
'''









