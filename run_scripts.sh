#!/bin/bash

/home/student/build/llvm/Release/bin/clang -I ~/build/klee/include -emit-llvm -c -g $1.c
/home/student/build/klee/Release+Asserts/bin/klee --write-sym-paths $1.bc
python executionTreeGenerator.py
