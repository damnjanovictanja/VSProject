#!/usr/bin/python

import sys, os, struct
from binarytree import Node

# ---------------- IVONA ----------------------
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
        raise IOError,'bad position'
    
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
# ------------ IVONA ----------------------





## ---------------------------------------------------------------------------------------------------
## ovo ce biti u main funkciji    
## Ovdje uneti putanju do symPaths.ts fajla ... 

## **** klee pokrenuti sa komandom -write-sym-paths ****

## otkomentarisati kasnije
#treeData = getPaths("klee-last/symPaths.ts") ## dobijamo mapu
#treeDataItems = treeData.items() # konvertujemo mapu u listu, radi lakseg obilaska i crtanja
#treeDataItems.sort() # sortiramo listu
#treeBranches = getTree(treeDataItems)
#print(treeBranches)


## -----------------------------------TESTIRANJE ZA CITANJE STABLA IZ LISTE---------------------------
lista0 = [(0, ''), (1, '1'), (2, '0')]
lista1 = [(0, ''), (1, '11'), (2, '01'), (3, '10'), (4, '00')]
lista2 = [(0, ''), (1, '11'), (2, '0'), (3, '10')]

stablo0 = getTree(lista0)
print(stablo0)
stablo1 = getTree(lista1)
print(stablo1)
stablo2 = getTree(lista2)
print(stablo2)

