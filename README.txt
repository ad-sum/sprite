Run this script on a Ubuntu VM with Python 2.7
1.Open terminal
2.Using text editor, enter desired MIPS instuctions into instructions.txt  
3.Copy instructions.txt and sprite_final.py into desired directory (cp ~/)
4.Navigate to the directory containing instruction.txt and sprite_final.py  (cd ~/)
5.Once in appropriate directory, enter the following command into the terminal: "python sprite_final.py"
6.Program is now executing in terminal and awaiting user input
7.Follow instructions listed in terminal to finish program execution

Processor configurations used for test cases.
last_use = [0]*31
re_load = 2
re_save = 5
re_add = 5
re_mult = 5
re_div = 5
re_add = [0]*31
re_mult = [0]*31
re_div = [0]*31
FT = [0]*31
k_load = 10+1 # number to show the cycles to finish an instruction- right now i gave them numbers to be easier to test the program- in the end the user should give us that number
k_save = 2+1
k_add = 3+1
k_branch = 3+1
k_mul = 7+1
k_div = 40+1

rob = 5
reg_in_use = [0]*31
FINISH = []
load_num = 0;save_num = 0; add_num = 0; mul_num = 0; div_num = 0; branch_num = 0
COMMIT = []
ISSUE = [1]
