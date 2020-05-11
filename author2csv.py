import json
import pandas as pd
f = open("D:\Aminer_Data\VID\Academic Social Network\Work\AMiner-Author.txt", encoding='UTF-8')
line = f.readline()
# E author
id_ls = []
name_ls = []
pc_ls = []
cn_ls = []
hi_ls = []
pi_ls = []
upi_ls = []

# E affiliation
all_aff_dict = {}
all_aff_ls = []
all_aff_id_ls = []

# E concept
all_cpt_dict = {}
all_cpt_ls = []
all_cpt_id_ls = []

# R author2affiliation
aa_author_id = []
aa_aff_id = []
aa_type = []

# R author2concept
ac_author_id = []
ac_cpt_id = []
ac_type = []


cnt = 0
ID = ''
while line:
    if '#index ' in line:
        ID = line[line.index(' ') + 1:].strip(' ').strip('\n')
        id_ls.append(ID)
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt)
    elif '#n ' in line:
        name = line[line.index(' ') + 1:].strip(' ').strip('\n')
        name_ls.append(name)
    elif '#a ' in line:
        raw_line = line[line.index(' ') + 1:].strip(' ').strip('\n')
        items = raw_line.split(';')
        for i in items:
            if i != '':
                if all_aff_dict.get(i, 'NONE') == 'NONE':
                    all_aff_dict[i] = str(len(all_aff_dict) + 1)
                aa_author_id.append(ID)
                aa_aff_id.append(all_aff_dict[i])

    elif '#pc ' in line:
        pc = line[line.index(' ') + 1:].strip(' ').strip('\n')
        pc_ls.append(pc)
    elif '#cn' in line:
        cn = line[line.index(' ') + 1:].strip(' ').strip('\n')
        cn_ls.append(cn)
    elif '#hi ' in line:
        hi = line[line.index(' ') + 1:].strip(' ').strip('\n')
        hi_ls.append(hi)
    elif '#pi ' in line:
        pi = line[line.index(' ') + 1:].strip(' ').strip('\n')
        pi_ls.append(pi)
    elif '#upi ' in line:
        upi = line[line.index(' ') + 1:].strip(' ').strip('\n')
        upi_ls.append(upi)
    elif '#t ' in line:
        raw_line = line[line.index(' ') + 1:].strip(' ').strip('\n')
        items = raw_line.split(';')
        for i in items:
            if i != '':
                if all_cpt_dict.get(i, 'NONE') == 'NONE':
                    all_cpt_dict[i] = str(len(all_cpt_dict) + 1)
                ac_author_id.append(ID)
                ac_cpt_id.append(all_cpt_dict[i])
    line = f.readline()

f.close()
print('Done:', cnt)

for key, val in all_aff_dict.items():
    all_aff_ls.append(key)
    all_aff_id_ls.append(val)

for key, val in all_cpt_dict.items():
    all_cpt_ls.append(key)
    all_cpt_id_ls.append(val)

aa_type = ['belong2'] * len(aa_aff_id)
ac_type = ['interest'] * len(ac_cpt_id)


dataframe = pd.DataFrame({"authorID:ID": id_ls, "name": name_ls, "pc:int": pc_ls, "cn:int": cn_ls, "hi:int": hi_ls,
                          "pi:float": pi_ls, "upi:float": upi_ls})
dataframe.to_csv(r"e_author.csv", sep=',', index=False)


dataframe2 = pd.DataFrame({"affiliationID:ID": all_aff_id_ls, "name": all_aff_ls})
dataframe2.to_csv(r"e_affiliation.csv", sep=',', index=False)

dataframe3 = pd.DataFrame({"conceptID:ID": all_cpt_id_ls, "name": all_cpt_ls})
dataframe3.to_csv(r"e_concept.csv", sep=',', index=False)

'''
# R author2affiliation
aa_author_id = []
aa_aff_id = []

# R author2concept
ac_author_id = []
ac_cpt_id = []
'''

dataframe4 = pd.DataFrame({":START_ID": aa_author_id, ":END_ID": aa_aff_id, ":TYPE": aa_type})
dataframe4.to_csv(r"r_author2affiliation.csv", sep=',', index=False)

dataframe5 = pd.DataFrame({":START_ID": ac_author_id, ":END_ID": ac_cpt_id, ":TYPE": ac_type})
dataframe5.to_csv(r"r_author2concept.csv", sep=',', index=False)
