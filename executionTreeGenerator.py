import os
import sys
import treeKlee as tk

# formiramo listu linija od interesa - koje se ticu linija source code-a u kojima su uslovi
# - to su linije oblika X lineNum X ... X Q X X X \n
def lineNumbersOfSourceCode():
  lines = []
  f = open("./klee-last/run.istats", "r")
  ind = 0
  while(True):
    currLine = f.readline();
    if(currLine[0:2] == "fn"): # currLine = "fn=..." - starting point of file run.istats
      break
  while(True):
    currLine = f.readline().split(' ')
    if(currLine[0][0:2] == "fn"): # when currLine = "fn=main", we need to stop
      break
    # Q = currLine[len(currLine)-5]
    if(len(currLine) > 4 and ind == 0 and currLine[len(currLine)-5] != '0'): # prvi uslov samo jednom
      lines.append(int(currLine[1]))
      ind = 1
    elif(len(currLine) > 4 and ind == 1 and currLine[len(currLine)-5] != '0'): # uslovi koji se ticu nezavisnih if-ova treba da se nadovezuju svuda, ovde ih uzimamo odgovarajuci broj puta (ali jos uvek nisu na adekvatnim indeksima...)
      for j in range (0, int(currLine[len(currLine)-5])):
        lines.append(int(currLine[1]))
  return lines

treeData = tk.getPaths("klee-last/symPaths.ts")
treeDataItems = treeData.items()
treeBranches = tk.getTree(treeDataItems)
preorder = treeBranches.PreorderTraversal(treeBranches) # KLD obilazak cvorova (uslovi, ali i listovi)
print("uslovi+listovi:\n",preorder)
preorder = tk.formConditionNodes(treeBranches, preorder) # -> KLD obilazak cvorova u kojima su uslovi
print("uslovi:\n",preorder)
mapPreorder = {} # mapiramo jer zelimo da budu uparene sa odgovarajucim linijama iz fajla "run.istats"
lines = lineNumbersOfSourceCode()
print("linije:\n",lines)
#for i in range (0, len(preorder)):
# moramo nekako obraditi kada postoji vise nezavisnih uslova... - tu su sve linije odgovarajuci broj puta, ali ne u odgovarajucem redosledu
#  mapPreorder[preorder[i]] = lines[i]



####################################################################
## Ovdje popunjavamo stablo informacijama o rednom broju linije gdje se nalazi uslov, mislim da je sada dobar redosled...
mapPreorder = tk.joinTreeAndLineNumbers(treeBranches, lines)
####################################################################


tk.drawTree(treeBranches, len(treeDataItems), mapPreorder)  
