import os
import sys
import treeKlee as tk

treeData = tk.getPaths("klee-last/symPaths.ts")
treeDataItems = treeData.items()
treeDataItems.sort()
treeBranches = tk.getTree(treeDataItems)
tk.drawTree(treeBranches, len(treeDataItems))

