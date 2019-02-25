#!/usr/bin/python

import sys, os, struct
from binarytree import Node
import matplotlib.pyplot as plt

# funkcija koja cita mapu iz symPaths.ts fajla:

def getPaths(path):
    data = open(path,'rb').read() # Otvaramo binarni fajl za citanje
    paths = { 0 : ''} # Mapa u kojoj cemo cuvati putanje
    pos = 0 # Indikator dokle smo stigli sa citanjem
    
    # prolazak kroz fajl i popunjavanje mape
    while pos<len(data):
        id,tag = struct.unpack('II', data[pos:pos+8])
        pos += 8
        if tag&(1<<31):
            child = tag ^ (1<<31)
            paths[child] = paths[id]
        else:
            size = tag
            paths[id] += data[pos:pos+size]
            pos += size
    if pos!=len(data):
        raise IOError
    
    return paths

# funkcija koja cita strukturu stabla iz liste:

# [(0, ''), (1, '1'), (2, '0')]
# Stablo:
#  /\

# [(0, ''), (1, '11'), (2, '01'), (3, '10'), (4, '00')]
# Stablo:
#  /\
# /\/\

# [(0, ''), (1, '11'), (2, '0'), (3, '10')]
# Stablo:
#  /\
#   /\

def getTree(treeList):
    root = Node(0)
    
    for i in range(1, len(treeList)):
        branch = (treeList[i])[1]
        tmp = root
        for j in range(0, len(branch)):
            if(branch[j] == '0'):
                if(not tmp.left):
                    tmp.left = Node(i)
                tmp = tmp.left
            elif(branch[j] == '1'):
                if(not tmp.right):
                    tmp.right = Node(i)
                tmp = tmp.right
    
    return root
    

# funkcija dobija strukturu stabla i iscrtava ga

def drawTree(tree):
    
    x = 0.5
    y = 0.9
    dx = 0.4
    dy = 0.08
    
    def drawLines(tree, x, y, dx, dy):
        dx = dx * 0.8
        dy = dy * 1.2
        if(tree.left and tree.right):
            plt.plot([x-dx,x,x+dx],[y-dy,y,y-dy], '-k')
            drawLines(tree.left, x-dx, y-dy, dx, dy)
            drawLines(tree.right, x+dx, y-dy, dx, dy)
        elif(tree.left):
            plt.plot([x-dx, x], [y-dy, y], '-k')
            drawLines(tree.left, x-dx, y-dy, dx, dy)
        elif(tree.right):
            plt.plot([x, x+dx], [y, y-dy],'-k')
            drawLines(tree.left, x+dx, y-dy, dx, dy)
         
    drawLines(tree, x, y, dx, dy)    
    plt.show()


