# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 08:32:26 2020

@author: Alexandra
"""
import numpy as np
class Layer(object):
    """One layer of HIS image"""
    
    def __init__(self,arr):
        """Constructor"""
        self.arr=arr
    
    def __str__(self):
        return str(self.arr)
    
    def __getitem__(self,key):
        return self.arr[key] 
    
    def __setitem__(self,key,value):
        self.arr[key] = value
    
    def __sub__(self, other):
        return Layer(self.arr - other.arr)
    
    def __truediv__(self, other):
        
        return Layer(self.arr / other.arr)
    
    def __or__(self,other):
        return Layer(np.logical_or(self.arr,other.arr))
    
    def __and__(self,other):
        return Layer(np.logical_and(self.arr,other.arr))
    
    # def __gt__(self,other):
    #     return Layer(self.arr > other)
    def __rshift__(self,other):
        if isinstance(other, self.__class__):
            return Layer(self.arr > other.arr)
        
        elif isinstance(other, float):
            return Layer(self.arr > other)

    # def __lt__(self, other):
    #     return Layer(self.arr < other)
    def __lshift__(self, other):
        if isinstance(other, self.__class__):
            return Layer(self.arr < other.arr)
        
        elif isinstance(other, float):
            return Layer(self.arr < other)
    
    def __eq__(self, other):
        return Layer( self.arr == other)
    
    def __invert__(self):
        return Layer(np.logical_not(self.arr))
    
    def __ne__(self, other):
        return(self.arr!=other)