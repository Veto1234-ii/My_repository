# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 23:20:42 2020

@author: Alexandra
"""

def getMTL(mtl):
    data={}
    
    with open(mtl) as file:
        for line in file:
            if line.find("GROUP", 0) == -1 and line.find("END", 0) == -1:
                l = line.replace("=","").split()
                data[l[0]] = l[1]
    return data

