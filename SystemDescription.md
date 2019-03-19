# Opis sistema

## Zadatak:

Korišćenjem informacija o simboličkom izvršavanju u
okviru alata KLEE napraviti vizuelni prikaz simboličkog izvršavanja,
odnosno automatski generisati prikaz stabla pretrage (sa detaljima o
stanju i putanjama u okviru čvorova) kao i omogućiti prikaz dela
stabla pretrage, odnosno prekidanje generisanja prikaza na osnovu nekog
zadatog parametra veličine stabla pretrage. Stablo pretrage moze da bude
ogromno, podrazumeva se da rešenje treba da radi za kratke programe koji
nemaju kompleksnu strukturu. 

## Arhitektura sistema (opis osnovnih modula implementacije):
  * get_execution_tree.sh:
    Pokreće alate **clang** i **klee** i nakon toga poziva skriptu *executionGenerator.py*.
  * executionTreeGenerator.py:
      * def lineNumbersOfSourceCode(mapLines): 
        Kreira listu linija izvornog *.c* koda u kojima se nalaze uslovi koji se smeštaju u stablo.
        Obrađuje argumente komandne linije pozivom funkcija iz *treeKlee.py*.
  * treeKlee.py:
    * def getPaths(path):
      Čita mapu iz *symPaths.ts* koja je značajna za strukturu stabla.
    * def getTree(treeList):
      Kreira stablo na osnovu mape.
    * def drawTree(tree, leaves, mapPreorder):
      Crta stablo.
    * def fillTheLeaves(tree, cond):
      Popunjava listove stabla.
    * def formConditionNodes(tree, preorder):
    * def joinTreeAndLineNumbers(root, lines, mapLines):
      Popunjava uslove stabla.
  

## Način razmišljanja (osnovne ideje, obrazloženja za ključne odluke, opis osnovnog algoritma):

* Korišćena je bash skripta koja generiše potrebne fajlove. 
* U bash skripti se pokreće **clang**, **klee**, a tek onda glavni program napisan u python-u.
* Korišćenjem alata **clang** dobija se *llvm kod*.
* Od tog llvm koda pokretanjem alata **klee** sa opcijom *--write-sym-paths* dobija se folder **klee-last** 
koji sadrzi fajlove u kojima se nalaze potrebne informacije.
* Za početak je bitan binarni fajl *symPaths.ts*. 
* U python programu **executionGenerator.py** se kao argument dobija putanja do *symPaths.ts* fajla.
* Čita se taj fajl pozivom funkcije *getPaths()* iz modula **treeKlee.py**.
* Od dobijene liste kreiramo stablo funkcijom *getTree()*. 
* Sledeći bitan fajl generisan od strane **klee** alata je *run.istats*.
* Iz tog fajla se dobijaju informacije o položaju uslova u stablu, 
kao i o rednom broju linije izvornog koda gde se nalazi uslov. 
* Prvo se uparuje redni broj linije sa uslovom pozivom funkcije *lineNumbersOfSourceCode()*, 
a nakon toga se popunjava stablo dobijenim uslovima koristeći funkciju *joinTreeAndLineNumbers()*



