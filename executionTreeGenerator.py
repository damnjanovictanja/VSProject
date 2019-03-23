import os
import sys
import treeKlee as tk
import re

# lines from the "run.istats" which are related to conditions from a source code are the following:
# X lineNum X ... X Q X X X \n
def lineNumbersOfSourceCode(mapLines):
  lines = []
  f = open("./klee-last/run.istats", "r")
  while(True):
    currLine = f.readline()
    if(currLine == ""):
      break
    currLine = currLine.split(' ')
    print(currLine)
    # fork = currLine[2] - toliko puta treba da se ponovi uslov u stablu...
    if(len(currLine) == 16 and currLine[2] != '0'):
      for j in range (0, int(currLine[3])):
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
    cond = v.find("if")+len("if")
    mapLines[k] = (mapLines[k])[cond:] # cond - index of '(' - which is after "if"
    mapLines[k] = (mapLines[k]).replace(" (", "(") # if (...) -> if(...)
    mapLines[k] = (mapLines[k]).replace(") {", "){") # if(...) { -> if(...){
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
#preorder = treeBranches.PreorderTraversal(treeBranches) # KLD obilazak cvorova (uslovi, ali i listovi)
#print("uslovi+listovi:\n",preorder)
#preorder = tk.formConditionNodes(treeBranches, preorder) # -> KLD obilazak cvorova u kojima su uslovi
#print("uslovi:\n",preorder)
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

#cond = ""
#tk.fillTheLeaves(treeBranches, cond)
tk.drawTree(treeBranches, len(treeDataItems))
#if (len(sys.argv) != 2):
#  tk.drawTree(treeBranches, len(treeDataItems))
#else:
#  tk.drawTree(treeBranches, len(treeDataItems), sys.argv[1])

