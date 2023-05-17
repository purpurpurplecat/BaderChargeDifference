import os
import numpy as np
import pandas as pd

charge = []
atom_num = []
element  = []
value = []
bader_charge = []
value_charge = []
transfer = []
auto_num = []

#reading elements in POSCAR
with open('POSCAR', 'r') as fff:
    POSCAR_lines = fff.readlines()
    element_line = POSCAR_lines[5]
    num_line = POSCAR_lines[6]
    element = element_line.split()
    for num in num_line.split():
        auto_num.append(int(num))
# print(element)

#reading value in POTCAR.The order is the same as the order in POSCAR
with open('POTCAR', 'r') as ff:
    POTCAR_lines = ff.readlines()
    re = os.popen("grep 'ZVAL' POTCAR").readlines()
    for n in range(0,len(re)):
        value.append(re[n].split('ZVAL   =   ')[-1].split('   mass and valenz')[0])
#print(re)
#print(value)

#reading bader charge
print('Plz conform the followings value in an order ')
print(value)

with open('ACF.dat', 'r') as f:
    lines = f.readlines()
    filtered_lines = lines[2:-4]
# print(filtered_lines)
    [charge.append(data.split()[4]) for data in filtered_lines]
    # print(charge)
    element_kind = int(input('How many kinds of elements in this system? :  '))

    for kind in range(1,element_kind + 1):
        # print(kind)
        sumchg = 0
        print('No.'+str(kind)+' element numbers:  ' + str(auto_num[kind - 1]))

        if kind == 1:
            for i in range(0,auto_num[kind - 1]):
                sumchg = sumchg + float(charge[i])
            print('No.' + str(kind) + ' elements total bader charge is ' + str(sumchg))
            
            value_charge.append(float(value[kind - 1]) * float(auto_num[kind - 1]))
            bader_charge.append(sumchg)
            # atom_num.append(element_num)
            transfer.append(float(value[kind - 1]) * float(auto_num[kind - 1]) - sumchg)
        else:
            
            start_atom = int(np.sum(auto_num[:(kind-1)]))
            end_atom = int(np.sum(auto_num[:kind]))
            # print(start_atom)
            # print(end_atom)
            for i in range(start_atom,end_atom):
                sumchg = sumchg + float(charge[i])
            print('No.' + str(kind) + ' elements total bader charge is ' + str(sumchg))
            value_charge.append(float(value[kind - 1]) * float(auto_num[kind - 1]))
            bader_charge.append(sumchg)
            transfer.append(float(value[kind - 1]) * float(auto_num[kind - 1]) - sumchg)

df = pd.DataFrame({'element':element,'atoms_num':auto_num,'value_charge':value_charge,'bader_charge':bader_charge,'transfer_charge':transfer})
df.to_csv('test.csv', index=False)
print(df)