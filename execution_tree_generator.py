'''
Main script for creating execution tree
'''

import sys
import tree_klee as tk

# lines from the "run.istats" which are related to conditions from a source code are the following:
# X lineNum X ... X Q X X X \n


def line_numbers_of_source_code(map_lines):
    '''
    Returns line numbers of source code according to run.istats file
    :param map_lines:
    :return:
    '''
    lines = []
    istats_file = open("./klee-last/run.istats", "r")
    while True:
        curr_line = istats_file.readline()
        if curr_line == "":
            break
        curr_line = curr_line.split(' ')
        # fork = curr_line[2] - toliko puta treba da se ponovi uslov u stablu...
        if len(curr_line) == 16 and curr_line[2] != '0':
            for _ in range(0, int(curr_line[3])):
                lines.append(int(curr_line[1]))
    # lines: n1, n2, ..., nk -> map_lines: {ni1:condition1, ni2:condition2, ..., nij:conditionk}
    # e.g. - lines: 1, 2, 2, 3, 3, 3, 3 -> map_lines: {1:c1, 2:c2, 3:c3}
    # opening a source code for the current test case
    istats_file.close()
    source_file = open("./test/" + sys.argv[1], "r")
    trial = source_file.read().split('\n')  # n. line has index n-1
    source_file.close()
    i = 0
    while i < len(lines):
        index = lines[i]
        map_lines[index] = trial[index-1]
        i += 1
    for key, value in map_lines.items():
        # if(x%5 == 0) -> (x%5 == 0)
        cond = value.find("if")+len("if")
        # cond - index of '(' - which is after "if"
        map_lines[key] = (map_lines[key])[cond:]
        map_lines[key] = (map_lines[key]).replace(
            " (", "(")  # if (...) -> if(...)
        # if(...) { -> if(...){
        map_lines[key] = (map_lines[key]).replace(") {", "){")
        # (x%5 == 0){ OR (x%5 == 0) -> x%5 == 0
        if (map_lines[key])[-1] == '{':
            map_lines[key] = (map_lines[key])[1:-2]  # remove "){"
        else:
            map_lines[key] = (map_lines[key])[1:-1]  # remove ")"
        # x%5 == 0 -> x%5 = 0
        map_lines[key] = (map_lines[key]).replace("==", "=")
    return lines


def main():
    '''
    Main program
    :return:
    '''
    tree_data = tk.get_paths("klee-last/symPaths.ts")
    tree_data_items = tree_data.items()
    tree_branches = tk.get_tree(tree_data_items)
    # # KLD obilazak cvorova (uslovi i listovi)
    # preorder = tree_branches.PreorderTraversal(tree_branches)
    # print("uslovi+listovi:\n",preorder)
    # # KLD obilazak cvorova u kojima su uslovi
    # preorder = tk.formConditionNodes(tree_branches, preorder)
    # print("uslovi:\n",preorder)
    map_of_lines = {}
    lines_numbers = line_numbers_of_source_code(map_of_lines)
    # for i in range (0, len(preorder)):
    # #moramo nekako obraditi kada postoji vise nezavisnih uslova...
    # # - tu su sve linije odgovarajuci broj puta, ali ne u odgovarajucem redosledu
    # 	map_preorder[preorder[i]] = lines[i]

    ####################################################################
    # Ovdje popunjavamo stablo informacijama o rednom broju linije gdje se nalazi uslov,
    # mislim da je sada dobar redosled...
    # mapa je ono sto nam treba, ali ne podrzava duplikate, pa nam treba
    # i lista i mapa istovremeno (lista ima dovoljan broj pojavljivanja svake linije,
    # a onda iz mape samo citamo te uslove...)
    tk.join_tree_and_line_numbers(tree_branches, lines_numbers, map_of_lines)
    ####################################################################

    # cond = ""
    # tk.fillTheLeaves(tree_branches, cond)

    if len(sys.argv) == 3:
        print("Drawing tree with limit: " + sys.argv[2])
        tk.draw_tree(tree_branches, len(tree_data_items), int(sys.argv[2]))
    else:
        tk.draw_tree(tree_branches, len(tree_data_items))


if __name__ == '__main__':
    main()
