#!/bin/bash
cd test
/home/student/build/llvm/Release/bin/clang -I ~/build/klee/include -emit-llvm -c -g $1.c
/home/student/build/klee/Release+Asserts/bin/klee --write-sym-paths $1.bc
cd ..
rm -rf klee-last
mkdir klee-last
cp ./test/klee-last/* ./klee-last/
python executionTreeGenerator.py
