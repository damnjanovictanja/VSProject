#!/usr/bin/python

import sys, os, struct

def getPaths(path):
    data = open(path,'rb').read() # Otvaramo binarni fajl za citanje
    paths = { 0 : ''} # Mapa u kojoj cemo cuvati putanje
    pos = 0 # Indikator dokle smo stigli sa citanjem
    
    # prolazak kroz fajl i popunjavanje mape
    while pos<len(data):
        id,tag = struct.unpack('II', data[pos:pos+8])
        #print(id, tag)
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
    #print("--------");
    return paths
    
## Ovdje uneti putanju do symPaths.ts fajla ... 
treeData = getPaths("klee-last/symPaths.ts") ## mapa

treeDataItems = treeData.items() # konvertujemo mapu u listu, radi lakseg obilaska i crtanja
treeDataItems.sort() # sortiramo listu

print(treeDataItems)

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
# /\


