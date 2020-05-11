import json
import pandas as pd
f = open("D:\Aminer_Data\VID\Academic Social Network\Work\AMiner-Coauthor.txt", encoding='UTF-8')

line = f.readline()
src_ls = []
tar_ls = []
weight_ls = []
cnt = 0
while line:
    string = line.replace('#', '').strip()
    src, tar, weight = string.split('	')

    src_ls.append(src)
    tar_ls.append(tar)
    weight_ls.append(weight)
    cnt += 1
    if cnt % 50000 == 0:
        print(cnt)
    line = f.readline()

f.close()
print('Done:', cnt)
type_ls = ['Collaborate'] * len(src_ls)
dataframe = pd.DataFrame({":START_ID": src_ls, ":END_ID": tar_ls, "n_cooperation": weight_ls, ":TYPE": type_ls})
dataframe.to_csv(r"r_coauthor.csv", sep=',', index=False)

