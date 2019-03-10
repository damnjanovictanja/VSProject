#!/usr/bin/python

from __future__ import division
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
    k = 1
    # ovde namestiti da oni sa istim uslovom da imaju isto k...?
    for i in range(1, len(treeList)):
        branch = (treeList[i])[1]
        tmp = root
        for j in range(0, len(branch)):
            if(branch[j] == '1'):
                if(not tmp.left):
                    tmp.left = Node(k) #i
		    k = k+1
                tmp = tmp.left
            elif(branch[j] == '0'):
                if(not tmp.right):
                    tmp.right = Node(k) #i
		    k = k+1
                tmp = tmp.right
    return root

# funkcija dobija strukturu stabla i iscrtava ga
def drawTree(tree, leaves, mapPreorder):
    
    def text(x, y, t, size=12, **kwargs):
        plt.text(x, y, t, ha='center', va='center', size=size, bbox=dict(boxstyle='round', ec='k', fc='w'), **kwargs)

    def drawLines(tree, x, y, dx, dy):
        preorder = tree.PreorderTraversal(tree)
        ind = False
        dx = dx * 0.5
        dy = dy * 1.2
        if(tree.left):
            ind = True
            text(x-dx/2, y-dy/2, "True", alpha=0.4)
            plt.plot([x-dx, x], [y-dy, y], '-k')
            drawLines(tree.left, x-dx, y-dy, dx, dy)
        if(tree.right):
            ind = True
            text(x+dx/2, y-dy/2, "False", alpha=0.4)
            plt.plot([x, x+dx], [y, y-dy],'-k')
            drawLines(tree.right, x+dx, y-dy, dx, dy)
        if(ind):
            text(x, y, mapPreorder[tree.data], 20) #"uslov"
        else:
            text(x, y, "list", 15)

    x = 0.5
    y = 1
    dx = 0.05*(2**(leaves-1))
    dy = 0.1
    drawLines(tree, x, y, dx, dy)    
    plt.show()

# funkcija za KLD obilazak stabla:
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def PreorderTraversal(self, root):
        res = []
        if root:
            res.append(root.data)
            res = res + self.PreorderTraversal(root.left)
            res = res + self.PreorderTraversal(root.right)
        return res

# preorder sadrzi i uslove i listove, sada formiramo listu koja sadrzi KLD obilazak samo uslova:
def formConditionNodes(tree, preorder):
  ind = False
  if(tree.left):
    ind = True
    formConditionNodes(tree.left, preorder)
  if(tree.right):
    ind = True
    formConditionNodes(tree.right, preorder)
  if(ind == False):
    preorder.remove(tree.data)
  return preorder
