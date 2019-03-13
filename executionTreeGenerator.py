import os
import sys
import treeKlee as tk
import re

# lines from the "run.istats" which are related to conditions from a source code are the following:
# X lineNum X ... X Q X X X \n
def lineNumbersOfSourceCode(mapLines):
  lines = []
  f = open("./klee-last/run.istats", "r")
  ind = 0
  while(True):
    currLine = f.readline()
    if(currLine[0:2] == "fn"): # currLine = "fn=..." - starting point of file run.istats
      break
  while(True):
    currLine = f.readline().split(' ')
    if(currLine[0][0:2] == "fn"): # when currLine = "fn=main", we need to stop
      break
    # Q = currLine[len(currLine)-5]
    if(len(currLine) > 4 and ind == 0 and currLine[len(currLine)-5] != '0'): # first condition - just once (it's the only one which can have Q != 1 but need to appear just once)
      lines.append(int(currLine[1]))
      ind = 1
    elif(len(currLine) > 4 and ind == 1 and currLine[len(currLine)-5] != '0'): # all other conditions which have Q != 0 need to appear Q times (those are independent conditions, and we need to append them on the adequate nodes of the current tree)
      for j in range (0, int(currLine[len(currLine)-5])):
        lines.append(int(currLine[1]))
  # lines: n1, n2, ..., nk -> mapLines: {ni1:condition1, ni2:condition2, ..., nij:conditionk}
  # e.g. - lines: 1, 2, 2, 3, 3, 3, 3 -> mapLines: {1:c1, 2:c2, 3:c3}
  sourceFile = open("./test/" + (sys.argv)[1], "r") # opening a source code for the current test case
  trial = sourceFile.read().split('\n') # n. line has index n-1
  i = 0
  while(i < len(lines)):
    index = lines[i]
    mapLines[index] = trial[index-1]
    i += 1
  for k, v in mapLines.items():
    # if(x%5 == 0) -> (x%5 == 0)
    cond = v.find("if")+len("if") # len("if") - da ne hardkodiramo 2, nego da se zna na sta mislimo...
    mapLines[k] = (mapLines[k])[cond:] # cond - index of '(' - which is after "if"
    # (x%5 == 0){ OR (x%5 == 0) -> x%5 == 0
    if((mapLines[k])[-1] == '{'):
      mapLines[k] = (mapLines[k])[1:-2] # remove "){"
    else:
      mapLines[k] = (mapLines[k])[1:-1] # remove ")"
    # x%5 == 0 -> x%5 = 0
    mapLines[k] = (mapLines[k]).replace("==", "=")
  return lines

treeData = tk.getPaths("klee-last/symPaths.ts")
treeDataItems = treeData.items()
treeBranches = tk.getTree(treeDataItems)
preorder = treeBranches.PreorderTraversal(treeBranches) # KLD obilazak cvorova (uslovi, ali i listovi)
print("uslovi+listovi:\n",preorder)
preorder = tk.formConditionNodes(treeBranches, preorder) # -> KLD obilazak cvorova u kojima su uslovi
print("uslovi:\n",preorder)
mapPreorder = {} # mapiramo jer zelimo da budu uparene sa odgovarajucim linijama iz fajla "run.istats"
mapLines = {}
lines = lineNumbersOfSourceCode(mapLines)
print("linije:\n",lines)
print("mapa:\n", mapLines)
#for i in range (0, len(preorder)):
# moramo nekako obraditi kada postoji vise nezavisnih uslova... - tu su sve linije odgovarajuci broj puta, ali ne u odgovarajucem redosledu
#  mapPreorder[preorder[i]] = lines[i]



####################################################################
## Ovdje popunjavamo stablo informacijama o rednom broju linije gdje se nalazi uslov, mislim da je sada dobar redosled...
mapPreorder = tk.joinTreeAndLineNumbers(treeBranches, lines, mapLines) # mapa je ono sto nam treba, ali ne podrzava duplikate, pa nam treba i lista i mapa istovremeno (lista ima dovoljan broj pojavljivanja svake linije, a onda iz mape samo citamo te uslove...)
####################################################################


tk.drawTree(treeBranches, len(treeDataItems), mapPreorder)  
