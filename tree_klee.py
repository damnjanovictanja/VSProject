'''
Functions to get execution_tree from klee and to draw tree
'''
from __future__ import division
import struct
import matplotlib.pyplot as plt

# funkcija koja cita mapu iz symPaths.ts fajla:


def get_paths(path):
    '''
    Get tree from binary filed provided from klee
    :param path: to binary file
    :return: klee tree paths
    '''
    data = open(path, 'rb').read()  # Otvaramo binarni fajl za citanje
    paths = {0: ''}  # Mapa u kojoj cemo cuvati putanje
    pos = 0  # Indikator dokle smo stigli sa citanjem
    # prolazak kroz fajl i popunjavanje mape
    while pos < len(data):
        identificator, tag = struct.unpack('II', data[pos:pos+8])
        pos += 8
        if tag & (1 << 31):
            child = tag ^ (1 << 31)
            paths[child] = paths[identificator]
        else:
            size = tag
            paths[identificator] += data[pos:pos+size]
            pos += size
    if pos != len(data):
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


def get_tree(tree_list):
    '''
    Get tree from list
    :param tree_list:
    :return:
    '''
    root = Node(0)
    k = 1
    for i in range(1, len(tree_list)):
        branch = (tree_list[i])[1]
        tmp = root
        for j in range(0, len(branch)):
            if branch[j] == '1':
                if not tmp.left:
                    tmp.left = Node(k)
                    tmp.leave = False
                    k = k+1
                tmp = tmp.left
            elif branch[j] == '0':
                if not tmp.right:
                    tmp.right = Node(k)
                    tmp.leave = False
                    k = k+1
                tmp = tmp.right
    return root

# funkcija dobija strukturu stabla i iscrtava ga


def draw_tree(file_name, execution_tree, leaves, limit=None):
    '''
    Draw tree from structure
    :param execution_tree:
    :param leaves:
    :param limit:
    :return:
    '''
    def text(x_coordinate, y_coordinate, t_arg, size=12, **kwargs):
        '''
        Fill tree nodes with text
        :param x_coordinate:
        :param y_coordinate:
        :param t_arg:
        :param size:
        :param kwargs:
        :return:
        '''
        plt.text(x_coordinate, y_coordinate, t_arg, ha='center', va='center', size=size,
                 bbox=dict(boxstyle='round', ec='k', fc='w'), **kwargs)

    def draw_lines(tree, x_coordinate, y_coordinate, d_x, d_y, limitation=None):
        '''
        Draw branches and nodes of execution tree
        :param tree:
        :param x_coordinate:
        :param y_coordinate:
        :param d_x:
        :param d_y:
        :param limitation:
        :return:
        '''
        if limitation is not None and limitation == 0:
            text(x_coordinate, y_coordinate, "...", alpha=0.4)
            return
        ind = False
        d_x = d_x * 0.5
        d_y = d_y * 1.2
        if tree.left:
            ind = True
            text(x_coordinate-d_x/2, y_coordinate-d_y/2, "True", alpha=0.4)
            plt.plot([x_coordinate-d_x, x_coordinate], [y_coordinate-d_y, y_coordinate], '-k')
            if limitation is None:
                draw_lines(tree.left, x_coordinate-d_x, y_coordinate-d_y, d_x, d_y, limitation)
            else:
                draw_lines(tree.left, x_coordinate-d_x, y_coordinate-d_y, d_x, d_y, limitation-1)
        if tree.right:
            ind = True
            text(x_coordinate+d_x/2, y_coordinate-d_y/2, "False", alpha=0.4)
            plt.plot([x_coordinate, x_coordinate+d_x], [y_coordinate, y_coordinate-d_y], '-k')
            if limitation is None:
                draw_lines(tree.right, x_coordinate+d_x, y_coordinate-d_y, d_x, d_y, limitation)
            else:
                draw_lines(tree.right, x_coordinate+d_x, y_coordinate-d_y, d_x, d_y, limitation-1)
        if ind:
            text(x_coordinate, y_coordinate, tree.data, 20)  # condition
        else:
            text(x_coordinate, y_coordinate, tree.data, 15)  # "leave"

    x_coord = 0.5
    y_coord = 1
    d_x = 0.05*(2**(leaves-1))
    d_y = 0.1
    if limit is None:
        draw_lines(execution_tree, x_coord, y_coord, d_x, d_y)
    else:
        draw_lines(execution_tree, x_coord, y_coord, d_x, d_y, limit)
    plt.savefig(file_name[:-2] + ".pdf", format='pdf', dpi=80)
    plt.show()


def fill_the_leaves(tree, cond):
    '''
    Fill leaves of the tree with summed conditions
    :param tree:
    :param cond:
    :return:
    '''
    ind = False
    if tree.left:
        ind = True
        if cond != "":
            fill_the_leaves(tree.left, cond + " && " + tree.data)
        else:
            fill_the_leaves(tree.left, tree.data)
    if tree.right:
        ind = True
        if cond != "":
            fill_the_leaves(tree.right, cond + " && !(" + tree.data + ")")
        else:
            fill_the_leaves(tree.right, "!(" + tree.data + ")")
    if not ind:
        tree.data = cond


# some useful data related to tree, and preorder tree traversal:
class Node:
    '''
    Node of the tree
    '''
    def __init__(self, data):
        '''
        Create Node of the tree
        :param data:
        '''
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
# def formConditionNodes(tree, preorder):
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

#############################################################################################
# Funkcija koja popunjava cvorove stabla


def join_tree_and_line_numbers(root, lines, map_lines):
    '''
    Merge tree with lines from source codes
    :param root:
    :param lines:
    :param map_lines:
    :return:
    '''
    def joinTALN(root, lines, n, cond):
        '''
        Helper function to merge tree with lines from source code
        :param root:
        :param lines:
        :param n:
        :param cond:
        :return:
        '''
        if not root.leave:
            x = 0
            for l in lines:
                if l > n:
                    x = l
                    break
            if not x == 0:
                root.data = map_lines[x]  # writing condition into a node
                lines.remove(x)
                if root.left:
                    if cond != "":
                        joinTALN(root.left, lines, x,
                                 cond + "\n&&\n" + root.data)
                    else:
                        joinTALN(root.left, lines, x, root.data)
                if root.right:
                    if cond != "":
                        joinTALN(root.right, lines, x, cond +
                                 "\n&&\n!(" + root.data + ")")
                    else:
                        joinTALN(root.right, lines, x, "!(" + root.data + ")")
            else:
                print("Some error....")
        if root.leave:
            root.data = cond

    joinTALN(root, lines, 0, "")
