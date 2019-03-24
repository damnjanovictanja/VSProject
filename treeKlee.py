#!/usr/bin/python

from __future__ import division
import sys, os, struct
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
    for i in range(1, len(treeList)):
        branch = (treeList[i])[1]
        tmp = root
        for j in range(0, len(branch)):
            if(branch[j] == '1'):
                if(not tmp.left):
                    tmp.left = Node(k)
                    tmp.leave = False
                    k = k+1
                tmp = tmp.left
            elif(branch[j] == '0'):
                if(not tmp.right):
                    tmp.right = Node(k)
                    tmp.leave = False
                    k = k+1
                tmp = tmp.right
    return root

# funkcija dobija strukturu stabla i iscrtava ga
def drawTree(tree, leaves, limitation=None):

    def text(x, y, t, size=12, **kwargs):
        plt.text(x, y, t, ha='center', va='center', size=size, bbox=dict(boxstyle='round', ec='k', fc='w'), **kwargs)

    def drawLines(tree, x, y, dx, dy, limitation=None):
        if (limitation is not None and limitation == 0):
            text(x, y, "...", alpha=0.4)
            return
        ind = False
        dx = dx * 0.5
        dy = dy * 1.2
        if(tree.left):
            ind = True
            text(x-dx/2, y-dy/2, "True", alpha=0.4)
            plt.plot([x-dx, x], [y-dy, y], '-k')
            if limitation is None:
	            drawLines(tree.left, x-dx, y-dy, dx, dy, limitation)
            else:
	            drawLines(tree.left, x-dx, y-dy, dx, dy, limitation-1)
        if(tree.right):
            ind = True
            text(x+dx/2, y-dy/2, "False", alpha=0.4)
            plt.plot([x, x+dx], [y, y-dy],'-k')
            if limitation is None:
	            drawLines(tree.right, x+dx, y-dy, dx, dy, limitation)
            else:
	            drawLines(tree.right, x+dx, y-dy, dx, dy, limitation-1)
        if(ind):
            text(x, y, tree.data, 20) # condition
        else:
            text(x, y, tree.data, 15) # "list"
	
    x = 0.5
    y = 1
    dx = 0.05*(2**(leaves-1))
    dy = 0.1
    if limitation is None:
        drawLines(tree, x, y, dx, dy)
    else:
        drawLines(tree, x, y, dx, dy, limitation)	
    plt.show()

def fillTheLeaves(tree, cond):
    ind = False
    if(tree.left):
        ind = True
        if(cond != ""):
	        fillTheLeaves(tree.left, cond + " && " + tree.data)
        else:
	        fillTheLeaves(tree.left, tree.data)
    if(tree.right):
        ind = True
        if(cond != ""):
	        fillTheLeaves(tree.right, cond + " && !(" + tree.data + ")")
        else:
	        fillTheLeaves(tree.right, "!(" + tree.data + ")")
    if(ind == False):
        tree.data = cond


# some useful data related to tree, and preorder tree traversal:
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        self.leave = True

#    def PreorderTraversal(self, root):
#        res = []
#        if root:
#            res.append(root.data)
#            res = res + self.PreorderTraversal(root.left)
#            res = res + self.PreorderTraversal(root.right)
#        return res

# the function PreorderTraversal give us conditions and leaves, but we need just conditions
# kasnije ce nam trebati i listovi...
#def formConditionNodes(tree, preorder):
#    ind = False
#    if(tree.left):
#        ind = True
#        formConditionNodes(tree.left, preorder)
#    if(tree.right):
#        ind = True
#        formConditionNodes(tree.right, preorder)
#    if(ind == False):
#        preorder.remove(tree.data)
#    return preorder

######################################################################################################
# Funkcija koja popunjava cvorove stabla
def joinTreeAndLineNumbers(root, lines, mapLines):
    def joinTALN(root, lines, n, cond):
        if(not root.leave):
            x = 0
            for l in lines:
                if(l>n):
                    x = l
                    break
            if(not x==0):
                root.data = mapLines[x] # writing condition into a node
                lines.remove(x)
                if(root.left):
                    if(cond != ""):
                        joinTALN(root.left, lines, x, cond + " && " + root.data)
                    else:
                        joinTALN(root.left, lines, x, root.data)
                if(root.right):
                    if(cond != ""):
                        joinTALN(root.right, lines, x, cond + " && !(" + root.data + ")")
                    else:
                        joinTALN(root.right, lines, x, "!(" + root.data + ")")
            else:
                print("Some error....")
        if(root.leave):
            root.data = cond       
    
    joinTALN(root, lines, 0, "")
