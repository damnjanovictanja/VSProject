import os
import sys
#import utils
import treeKlee as tk

treeData = tk.getPaths("klee-last/symPaths.ts")
treeDataItems = treeData.items()
treeDataItems.sort()
treeBranches = tk.getTree(treeDataItems)
print(treeBranches)
#drawTree(treeBranches, "tree.png")
