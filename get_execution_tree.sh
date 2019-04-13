#!/bin/bash
cd test
/home/student/build/llvm/Release/bin/clang-format -i $1.c
/home/student/build/llvm/Release/bin/clang -I ~/build/klee/include -emit-llvm -c -g $1.c
/home/student/build/klee/Release+Asserts/bin/klee --write-sym-paths $1.bc
cd ..
rm -rf klee-last
mkdir klee-last
cp ./test/klee-last/* ./klee-last/
if [ "$#" -eq 1 ]; then
python execution_tree_generator.py $1.c # we need name of a source code - because we are writing conditions from it
fi
if [ "$#" -eq 2 ]; then
python execution_tree_generator.py $1.c $2
fi
cd results
eog $1.png
cd ..
