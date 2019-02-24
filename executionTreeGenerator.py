import os
import sys
import utils
import treeKlee

treeData = getPaths("klee-last/symPaths.ts")
treeDataItems = treeData.items()
treeDataItems.sort()
treeBranches = getTree(treeDataItems)
drawTree(treeBranches, "tree.png")
