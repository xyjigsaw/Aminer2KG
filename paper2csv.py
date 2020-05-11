import json
import re
import pandas as pd
f = open("D:\Aminer_Data\VID\Academic Social Network\Work\AMiner-Paper.txt", encoding='UTF-8')
line = f.readline()
# E paper
pid_ls = []
title_ls = []
year_ls = []
abs_ls = []

# E venue
all_vue_dict = {}
all_vue_ls = []
all_vue_id_ls = []

# R paper2venue
pv_paper_id = []
pv_vue_id = []
pv_type = []

# R citation
pp_start_id = []
pp_end_id = []
pp_type = []


cnt = 0

ID = ''
title = ''
year = ''
abstract = ''
raw_line = None
dstID = []

cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^(^)^.^\s]")

while line:
    if '#index ' in line:
        ID = line[line.index(' ') + 1:].strip(' ').strip('\n')
    if '#* ' in line:
        title = line[line.index(' ') + 1:].strip(' ').strip('\n')
        title.replace('\\', '').replace('\n', '.').replace("\"", '').replace("'", '')
        title = cop.sub('', title)
    if '#t ' in line:
        year = line[line.index(' ') + 1:].strip(' ').strip('\n')
    if '#! ' in line:
        abstract = line[line.index(' ') + 1:].strip(' ').strip('\n')
        abstract.replace('\\', '').replace('\n', '.').replace("\"", '').replace("'", '')
        abstract = cop.sub('', abstract)
    if '#c ' in line:
        raw_line = line[line.index(' ') + 1:].strip(' ').strip('\n')
    if '#%' in line:
        dstID.append(line[line.index(' ') + 1:].strip(' ').strip('\n'))
    if line == '\n':
        pid_ls.append(ID)
        title_ls.append(title)
        year_ls.append(year)
        abs_ls.append(abstract)
        items = raw_line.split(';')
        for i in items:
            if i != '':
                i.replace('\\', '').replace('\n', '.').replace("\"", '').replace("'", '')
                if all_vue_dict.get(i, 'NONE') == 'NONE':
                    all_vue_dict[i] = str(len(all_vue_dict) + 1)
                pv_paper_id.append(ID)
                pv_vue_id.append(all_vue_dict[i])
        for i in dstID:
            pp_start_id.append(ID)
            pp_end_id.append(i)
        ID = ''
        title = ''
        year = ''
        abstract = ''
        raw_line = None
        dstID = []
        cnt += 1
        if cnt % 5000 == 0:
            print(cnt)
    line = f.readline()

f.close()
print('Done:', cnt)


for key, val in all_vue_dict.items():
    all_vue_ls.append(key)
    all_vue_id_ls.append(val)

pv_type = ['belong2'] * len(pv_paper_id)
pp_type = ['refer'] * len(pp_start_id)


dataframe = pd.DataFrame({"paperID:ID(paperID)": pid_ls, "title:LABEL": title_ls, "year": year_ls, "abstract": abs_ls})
dataframe.to_csv(r"e_paper.csv", sep=',', index=False)


dataframe2 = pd.DataFrame({"venueID:ID(venueID)": all_vue_id_ls, "name:LABEL": all_vue_ls})
dataframe2.to_csv(r"e_venue.csv", sep=',', index=False)

dataframe3 = pd.DataFrame({":START_ID": pv_paper_id, ":END_ID": pv_vue_id, ":TYPE": pv_type})
dataframe3.to_csv(r"r_paper2venue.csv", sep=',', index=False)

dataframe4 = pd.DataFrame({":START_ID": pp_start_id, ":END_ID": pp_end_id, ":TYPE": pp_type})
dataframe4.to_csv(r"r_citation.csv", sep=',', index=False)
