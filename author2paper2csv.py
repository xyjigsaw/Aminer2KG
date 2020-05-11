import json
import pandas as pd
f = open("D:\Aminer_Data\VID\Academic Social Network\Work\AMiner-Author2Paper.txt", encoding='UTF-8')

line = f.readline()
src_ls = []
tar_ls = []
pos_ls = []
type_ls = []
cnt = 0
while line:
    _, src, tar, pos = line.split('	')

    src_ls.append(src)
    tar_ls.append(tar)
    pos_ls.append(pos.strip('\n'))
    cnt += 1
    if cnt % 50000 == 0:
        print(cnt)
    line = f.readline()

f.close()
type_ls = ['own'] * len(src_ls)
print('Done:', cnt)

dataframe = pd.DataFrame({":START_ID": src_ls, ":END_ID": tar_ls, "author_position": pos_ls, ":TYPE": type_ls})
dataframe.to_csv(r"r_author2paper.csv", sep=',', index=False)
