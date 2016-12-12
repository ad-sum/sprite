import sys
from sys import argv
#!/usr/bin/python
global load_num; global save_num ; global add_num; global mul_num; global div_num; global branch_num
# *_num show when the load or the save is going to be finished-so this number is going to be added with the cycle periods
global COMMIT# This keeps all of the commits
global commit# This keeps the commit of each each functional unit (FU)
global reg # an array simulating registers
global memory #an array simulating memory
global FT # an array simulating flouting point registers
global last_use # an array to show when the registry is going to be free, its index is the same as the FT
global i # the main iterator
global k_load ;global k_add; global k_mul; global k_div; global k_save; global k_branch
# k_* contains number of cycles FU takes to complete instuction
global re_load; global re_save; global re_add; global re_mult; global re_div;
# re_* define the amount of reservation station (RS) space for each FU
global issue_load;global finish_load; global issue_save;global finish_save;
global issue_add;global finish_add; global issue_mul;global finish_mul;
global issue_div;global finish_div
# issue_* stores the number of the issue cycle for that FU, the finish_* does the same for finish
issue_load = []; issue_save = []; issue_add = []; issue_mul = []; issue_div = []
finish_load = []; finish_save = []; finish_add = []; finish_mul = []; finish_div = []
# empty arrays set initial values
global ISSUE # stores issue number for the final instruction
global FINISH # stores the wite-back number for the final instruction
global cal_com
global reg_in_use # stores the cycle number when each register will become available
global rob # number of re-order buffers
rob = input("please enter the number of ROB:")
reg_in_use = [0]*31
FINISH = []
cal_com = []
load_num = 0;save_num = 0; add_num = 0; mul_num = 0; div_num = 0; branch_num = 0
COMMIT = []
ISSUE = [1]
memory = [45,12,0,0,10,135,254,127,18,4,55,8,2,98,13,5,233,158,167] # memory values Ivan gave us in the project
reg = [5]*31
last_use = [0]*31
re_load = input("please enter the number of reservation stations for load:")
re_save = input("please enter the number of reservation stations for save:")
re_add = input("please enter the number of reservation stations for add:")
re_mult = input("please enter the number of reservation stations for mult:")
re_div = input("please enter the number of reservation stations for division:")
FT = [0]*31
k_load = input("please enter the cycle number which takes to complete load:")
k_save = input("please enter the cycle number which takes to complete save:")
k_add = input("please enter the cycle number which takes to complete add:")
k_branch = input("please enter the cycle number which takes to complete branch:")
k_mul = input("please enter the cycle number which takes to complete mult:")
k_div = input("please enter the cycle number which takes to complete div:")
commit = 0
iss = []
flag = 0

def ROB (num):
    global COMMIT; global ISSUE; global FINISH; global rob; global flag
    if flag == 1: # for branches to change the issue value when we do wrong prediction
        num = FINISH[len(FINISH)-1]+1
        flag = 0
    co = [];
    b = 0
    for j in range(0, len(COMMIT)):
        if (num >= FINISH[j]) & (num <= COMMIT[j]): # check to see how many ROB slots available
            b += 1
            co.append(COMMIT[j])
    co = sorted(co)
    if b == rob:
        num = co[0] # if no ROB slots avaialbe wait for the earliest commit cycle
    return num

def Reservation (num,start,fin,which_instruct):
    global COMMIT; global FINISH; global re_load; global flag; global load_num;global i;
    global re_load; global re_save; global re_add; global re_mult; global re_div
    b = 0
    if which_instruct == 1: # check to see which instruction is using RS
        reservation_number = re_load
    if which_instruct == 2:
        reservation_number = re_save
    if which_instruct == 3:
        reservation_number = re_add
    if which_instruct == 4:
        reservation_number = re_mult
    if which_instruct == 5:
        reservation_number = re_div
    for j in range(0, len(start)):
        if (num >= start[j]) & (num <= fin[j]): # checks for number of avaiable RS at the cycle of issue
            b+=1
    issue = ISSUE[i] + 1
    if b == reservation_number:
        issue = max((ISSUE[i] + 1), fin[len(fin)-1]) # if all RS are full, wait for a RS to finish WB
    return issue

def load (instruct): # FU functions are fairly similar in organization
    global load_num ;global COMMIT;global commit;global reg ;global memory ;global last_use
    global FT ;global i ;global k_load ;global ISSUE ;global FINISH;global reg_in_use
    global re_load; global issue_load;global finish_load; global cal_com
    # for issue we have only one unit- so we should be sure that there is no loads before. the max between the last load or the ith instruction
    which_instruct = 1 # shows what instruction we have on hand to the reservation station
    load_num = ROB(ISSUE[len(ISSUE)-1]) #gives back the last issue number
    load_num = Reservation(load_num,issue_load,finish_load,which_instruct)
    ISSUE.append(load_num)
    load_num-=1
    issue_load.append(load_num)
    reg_name = (instruct.split()[1]).replace("F","")[0] # FT address to load to
    add = instruct.split()[2]
    offset = add.split("(")[0] # address offset
    mem = ((add.replace(")","")).split("(")[1]).split("$")[1] # memory address to load from which is in $*
    FT[int(reg_name)] = memory[(int(offset)+reg[int(mem)])] # loading
    load_num = max(last_use[int(reg_name)],load_num)+k_load # waiting for the registry to be free and issue- add the cycles its gana take
    cal_com.append(load_num)
    finish_load.append(load_num+1)
    FINISH.append(load_num+1)
    last_use[int(reg_name)] = load_num+1 # save the number when this FT is going to be free, load is finished
    commit = max(load_num+1 , commit) +1 # when to commit
    COMMIT.append(commit)

def save (instruct):
    global save_num ;global COMMIT;global commit;global reg ;global memory ;global cal_com
    global last_use ;global FT ;global i ;global k_save ;global ISSUE ;global FINISH;global reg_in_use
    which_instruct = 2
    save_num = ROB(save_num)
    save_num = Reservation(save_num, issue_save, finish_save,which_instruct)
    ISSUE.append(save_num)
    save_num-=1
    issue_save.append(save_num)
    reg_name = (instruct.split()[1]).replace("F","")[0]
    add = instruct.split()[2]
    offset = add.split("(")[0]
    mem = ((add.replace(")","")).split("(")[1]).split("$")[1]
    memory[(int(offset)+reg[int(mem)])] = FT[int(reg_name)]
    save_num = max(last_use[int(reg_name)],save_num)+k_save # if save is just reading FT, then no need for last_use to be updated
    cal_com.append(save_num)
    finish_save.append(save_num+1)
    FINISH.append(save_num+1)
    commit = max(save_num+1 , commit) +1
    COMMIT.append(commit)

def add (instruct):
    global add_num ;global COMMIT;global commit;global reg ;global memory ;global last_use ;global cal_com
    global FT ;global i ;global k_add ;global ISSUE ;global FINISH;global reg_in_use
    which_instruct = 3
    add_num = ROB(add_num)
    add_num = Reservation(add_num, issue_add, finish_add, which_instruct)
    ISSUE.append(add_num)
    add_num-=1
    issue_add.append(add_num)
    reg_name1 = (instruct.split()[1]).replace("$","")[0]
    reg_name2 = (instruct.split()[2]).replace("$","")[0]
    reg_name3 = (instruct.split()[3]).replace("$","")[0]
    reg[int(reg_name1)] = reg[int(reg_name2)]+reg[int(reg_name3)]
    add_num = max(reg_in_use[int(reg_name1)],reg_in_use[int(reg_name2)],reg_in_use[int(reg_name3)],add_num)+k_add
    cal_com.append(add_num)
    finish_add.append(add_num+1)
    FINISH.append(add_num+1)
    last_use[int(reg_name1)] = add_num+1
    commit = max(add_num+1 , commit) +1
    COMMIT.append(commit)

def addi(instruct):
    global add_num ;global COMMIT;global commit;global reg ;global memory ;global last_use ;global cal_com
    global FT ;global i ;global k_add ;global ISSUE ;global FINISH;global reg_in_use
    which_instruct = 3
    add_num = ROB(add_num)
    add_num = Reservation(add_num, issue_add, finish_add, which_instruct)
    ISSUE.append(add_num)
    add_num-=1
    issue_add.append(add_num)
    reg_name1 = (instruct.split()[1]).replace("$","")[0]
    reg_name2 = (instruct.split()[2]).replace("$","")[0]
    reg_name3 = (instruct.split()[3])
    reg[int(reg_name1)] = reg[int(reg_name2)]+int(reg_name3)
    add_num = max(reg_in_use[int(reg_name1)],reg_in_use[int(reg_name2)],add_num)+k_add
    cal_com.append(add_num)
    finish_add.append(add_num+1)
    FINISH.append(add_num+1)
    last_use[int(reg_name1)] = add_num+1
    commit = max(add_num+1 , commit) +1
    COMMIT.append(commit)

def addd (instruct) :
    global add_num ;global COMMIT;global commit;global reg ;global memory ;global last_use ;global cal_com
    global FT ;global i ;global k_add ;global ISSUE ;global FINISH;global reg_in_use
    which_instruct = 3
    add_num = ROB(add_num)
    add_num = Reservation(add_num, issue_add, finish_add, which_instruct)
    ISSUE.append(add_num)
    add_num-=1
    issue_add.append(add_num)
    reg_name1 = (instruct.split()[1]).replace("F","")[0]
    reg_name2 = (instruct.split()[2]).replace("F","")[0]
    reg_name3 = (instruct.split()[3]).replace("F","")[0]
    FT[int(reg_name1)] = FT[int(reg_name2)]+FT[int(reg_name3)]
    add_num = max(last_use[int(reg_name1)],last_use[int(reg_name2)],last_use[int(reg_name3)],add_num)+k_add
    cal_com.append(add_num)
    finish_add.append(add_num+1)
    FINISH.append(add_num+1)
    last_use[int(reg_name1)] = add_num+1
    commit = max(add_num+1 , commit) +1
    COMMIT.append(commit)

def subd (instruct):
    global add_num ;global COMMIT;global commit;global reg ;global memory ;global last_use ;global cal_com
    global FT ;global i ;global k_add ;global ISSUE ;global FINISH;global reg_in_use
    which_instruct = 3
    add_num = ROB(add_num)
    add_num = Reservation(add_num, issue_add, finish_add, which_instruct)
    ISSUE.append(add_num)
    add_num-=1
    issue_add.append(add_num)
    reg_name1 = (instruct.split()[1]).replace("F","")[0]
    reg_name2 = (instruct.split()[2]).replace("F","")[0]
    reg_name3 = (instruct.split()[3]).replace("F","")[0]
    FT[int(reg_name1)] = FT[int(reg_name2)]-FT[int(reg_name3)]
    add_num = max(last_use[int(reg_name1)],last_use[int(reg_name2)],last_use[int(reg_name3)],add_num)+k_add
    cal_com.append(add_num)
    finish_add.append(add_num+1)
    FINISH.append(add_num+1)
    last_use[int(reg_name1)] = add_num+1
    commit = max(add_num+1 , commit) +1
    COMMIT.append(commit)

def subi(instruct):
    global add_num ;global COMMIT;global commit;global reg ;global memory ;global last_use ;global cal_com
    global FT ;global i ;global k_add ;global ISSUE ;global FINISH;global reg_in_use
    which_instruct = 3
    add_num = ROB(add_num)
    add_num = Reservation(add_num, issue_add, finish_add, which_instruct)
    ISSUE.append(add_num)
    add_num-=1
    issue_add.append(add_num)
    reg_name1 = (instruct.split()[1]).replace("F","")[0]
    reg_name2 = (instruct.split()[2]).replace("F","")[0]
    reg_name3 = (instruct.split()[3])
    FT[int(reg_name1)] = FT[int(reg_name2)]-int(reg_name3)
    add_num = max(last_use[int(reg_name1)],reg_in_use[int(reg_name2)],add_num)+k_add
    cal_com.append(add_num)
    finish_add.append(add_num+1)
    FINISH.append(add_num+1)
    last_use[int(reg_name1)] = add_num+1
    commit = max(add_num+1 , commit) +1
    COMMIT.append(commit)

def multd(instruct):
    global mul_num ;global COMMIT;global commit;global reg ;global memory ;global last_use ;global cal_com
    global FT ;global i ;global k_mul ;global ISSUE ;global FINISH;global reg_in_use
    which_instruct = 4
    mul_num = ROB(mul_num)
    mul_num = Reservation(mul_num, issue_mul, finish_mul, which_instruct)
    ISSUE.append(mul_num)
    mul_num-=1
    issue_mul.append(mul_num)
    ISSUE.append(mul_num)
    reg_name1 = (instruct.split()[1]).replace("F","")[0]
    reg_name2 = (instruct.split()[2]).replace("F","")[0]
    reg_name3 = (instruct.split()[3]).replace("F","")[0]
    FT[int(reg_name1)] = FT[int(reg_name2)]*FT[int(reg_name3)]
    mul_num = max(last_use[int(reg_name1)],last_use[int(reg_name2)],last_use[int(reg_name3)],mul_num)+k_mul
    cal_com.append(mul_num)
    finish_mul.append(mul_num+1)
    FINISH.append(mul_num+1)
    last_use[int(reg_name1)] = mul_num+1
    commit = max(mul_num+1 , commit) +1
    COMMIT.append(commit)

def divd(instruct):
    global div_num ;global COMMIT;global commit;global reg ;global memory ;global last_use ;global cal_com
    global FT ;global i ;global k_div ;global ISSUE ;global FINISH;global reg_in_use
    which_instruct = 5
    div_num = ROB(div_num)
    div_num = Reservation(div_num, issue_div, finish_div, which_instruct)
    ISSUE.append(div_num)
    div_num-=1
    issue_div.append(div_num)

    reg_name1 = (instruct.split()[1]).replace("F","")[0]
    reg_name2 = (instruct.split()[2]).replace("F","")[0]
    reg_name3 = (instruct.split()[3]).replace("F","")[0]
    FT[int(reg_name1)] = FT[int(reg_name2)]/FT[int(reg_name3)]
    div_num = max(last_use[int(reg_name1)],last_use[int(reg_name2)],last_use[int(reg_name3)],div_num)+k_div
    cal_com.append(div_num)
    finish_div.append(div_num+1)
    FINISH.append(div_num+1)
    last_use[int(reg_name1)] = div_num+1
    commit = max(div_num+1 , commit) +1
    COMMIT.append(commit)

def beq (instruct):
    global branch_num ;global COMMIT;global commit;global reg ;global memory ;global last_use ;global cal_com
    global FT ;global i  ;global ISSUE ;global FINISH;global reg_in_use
    global flag
    branch_num = max (ISSUE[i],branch_num)+1
    ISSUE.append(branch_num)
    reg_name1 = (instruct.split()[1]).replace("$","")[0]
    reg_name2 = (instruct.split()[2]).replace("$","")[0]
    reg_name3 = (instruct.split()[3])
    if reg[int(reg_name1)] == reg[int(reg_name2)]: # if prediction is correct, don't wait and issue instructions in order
        i = int(reg_name3)-2
    else: # if prediciton is incorrect, wait until prediction finishes and then jump
        flag = 1
    branch_num = max(last_use[int(reg_name1)], last_use[int(reg_name2)], last_use[int(reg_name3)],branch_num) + k_branch
    cal_com.append(branch_num)
    FINISH.append(branch_num+1)
    commit = max(branch_num+1 , commit) + 1
    COMMIT.append(commit)

def bne (instruct):
    global branch_num ;global COMMIT;global commit;global reg ;global memory ;global last_use ;global cal_com
    global FT ;global i  ;global ISSUE ;global FINISH;global reg_in_use
    global flag
    branch_num = max (ISSUE[i],branch_num)+1
    ISSUE.append(branch_num)
    reg_name1 = (instruct.split()[1]).replace("$","")[0]
    reg_name2 = (instruct.split()[2]).replace("$","")[0]
    reg_name3 = (instruct.split()[3])
    if reg[int(reg_name1)] != reg[int(reg_name2)]:
        i = int(reg_name3)-2
    else:
        flag = 1
    branch_num = max(last_use[int(reg_name1)], last_use[int(reg_name2)], last_use[int(reg_name3)],branch_num) + k_branch
    cal_com.append(branch_num)
    FINISH.append(branch_num+1)
    commit = max(branch_num+1 , commit) + 1
    COMMIT.append(commit)

################################################################################
#main()
file = []
try:
    with open('instructions.txt', 'r') as file:
        file_contents = file.read()
    file_contents = file_contents.replace(",", "")
    file = file_contents.split("\n")
except :
    file1 = sys.stdin.readlines()
    file = []
    for i in file1:
        i = i.replace("\n","")
        i = i.replace(",","")
        file.append(i)
i = 0
z = 1
wat_do = []
while z:
    instruct = file[i]
    wat_do.append((instruct.split())[0])
    try :
        if wat_do[i] == "LD":
            load(instruct)
        elif wat_do[i] == "SD":
            save(instruct)
        elif wat_do[i] == "ADD":
            add(instruct)
        elif wat_do[i] == "ADDI":
            addi(instruct)
        elif wat_do[i] == "ADD.D":
            addd(instruct)
        elif wat_do[i] == "SUB.D":
            subd(instruct)
        elif wat_do[i] == "SUBI":
            subi(instruct)
        elif wat_do[i] == "MULT.D":
            multd(instruct)
        elif wat_do[i] == "DIV.D":
            divd(instruct)
        elif wat_do[i] == "BEQ":
            beq(instruct)
        elif wat_do[i] == "BNE":
            bne(instruct)
        else :
            k = 'k'+2
    except IOError:
        print ("instruction not preset : Error loading the instruction, compile Error")
    i = i+1
    if i>(len(file)-1):
        z = 0
for j in range(1,len(ISSUE)):
    iss.append(ISSUE[j]-1)
print ("Issue"+str(iss))
print ("Finish time"+str(cal_com))
print ("WB time"+str(FINISH))
print ("Commit time"+str(COMMIT))
print ("FP register"+str(FT))
print ("Int register"+str(reg))