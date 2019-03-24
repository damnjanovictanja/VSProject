# VSProject
MSc project, course: Software Verification

## Authors:
* Ivona Jurošević 1016/2018
* Tamara Marčetić 1040/2018
* Tatjana Damnjanović 1046/2018

### In order to execute program, you should install:
* python version 2.7 or higher
* Clang
* KLEE
* llvm
* **Note**: If using VM, above three are already installed.
* python library "binarytree"
	* could be installed using pip command:
		* pip install binarytree
		* for VM: pip install --user binarytree
			* *Note*: if pip is not installed, on Linux OS it can be installed with command:
				* sudo apt install python-pip
* python library "mathplotlib"
	* could be installed using following command:
		* sudo apt-get build-dep python-matplotlib
		* for VM: pip install --user matplotlib
* python library python-tk
	* sudo apt-get install python-tk
	
### Test examples are placed in folder test

### Run program using ./get_execution_tree.sh $PROGRAM_NAME $LIMIT

* *Note*: Every program should be placed in folder test!
* *Note*: $PROGRAM_NAME should not contain extensions.
* *Note*: $LIMIT can be any number to limit tree size.
	  If $LIMIT is not set, whole execution tree would be drawn out.
* *Example*: ./get_execution_tree.sh even_sym 3    
