# Name: data4embedding
# Author: Reacubeth
# Time: 2020/3/31 10:51
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import csv
import random
write_out = []
with open('DATA/r_author2affiliation.csv', 'r') as f:
    reader = csv.reader(f)
    flag = False
    for row in reader:
        if not flag:
            flag = True
            continue
        tmp = 'authorID' + row[0] + '\t' + '_author2affiliation_' + '\taffiliationID' + row[1]
        write_out.append(tmp)

print('r_author2affiliation.csv Read Done.')


with open('DATA/r_author2concept.csv', 'r') as f:
    reader = csv.reader(f)
    flag = False
    for row in reader:
        if not flag:
            flag = True
            continue
        tmp = 'authorID' + row[0] + '\t' + '_author2concept_' + '\tconceptID' + row[1]
        write_out.append(tmp)

print('r_author2concept.csv Read Done.')


with open('DATA/r_author2paper.csv', 'r') as f:
    reader = csv.reader(f)
    flag = False
    for row in reader:
        if not flag:
            flag = True
            continue
        tmp = 'authorID' + row[0] + '\t' + '_author2paper_' + '\tpaperID' + row[1]
        write_out.append(tmp)

print('r_author2paper.csv Read Done.')


with open('DATA/r_citation.csv', 'r') as f:
    reader = csv.reader(f)
    flag = False
    for row in reader:
        if not flag:
            flag = True
            continue
        tmp = 'paperID' + row[0] + '\t' + '_cites_' + '\tpaperID' + row[1]
        write_out.append(tmp)

print('r_citation.csv Read Done.')


with open('DATA/r_coauthor.csv', 'r') as f:
    reader = csv.reader(f)
    flag = False
    for row in reader:
        if not flag:
            flag = True
            continue
        tmp = 'authorID' + row[0] + '\t' + '_collaborates_with_' + '\tauthorID' + row[1]
        write_out.append(tmp)
        tmp = 'authorID' + row[1] + '\t' + '_collaborates_with_' + '\tauthorID' + row[0]
        write_out.append(tmp)

print('r_coauthor.csv Read Done.')


with open('DATA/r_paper2venue.csv', 'r') as f:
    reader = csv.reader(f)
    flag = False
    for row in reader:
        if not flag:
            flag = True
            continue
        tmp = 'paperID' + row[0] + '\t' + '_paper2venue_' + '\tvenueID' + row[1]
        write_out.append(tmp)

print('r_paper2venue.csv Read Done.')


random.shuffle(write_out)

train = write_out[:int(len(write_out) / 100 * 98)]
rest = write_out[int(len(write_out) / 100 * 98):]
del write_out

test = rest[:int(len(rest) / 2)]
valid = rest[int(len(rest) / 2):]


all_len = len(train)
print('All len:', all_len)
file_write_obj = open("train.txt", 'a+', encoding='utf-8')
cnt = 0
for var in train:
    cnt += 1
    file_write_obj.writelines(var)
    file_write_obj.write('\n')
    if cnt % 100000 == 0:
        print('{}/{}'.format(cnt, all_len))

print('Train Done')


all_len = len(test)
print('All len:', all_len)
file_write_obj = open("test.txt", 'a+', encoding='utf-8')
cnt = 0
for var in test:
    cnt += 1
    file_write_obj.writelines(var)
    file_write_obj.write('\n')
    if cnt % 100000 == 0:
        print('{}/{}'.format(cnt, all_len))

print('Test Done')


all_len = len(valid)
print('All len:', all_len)
file_write_obj = open("valid.txt", 'a+', encoding='utf-8')
cnt = 0
for var in valid:
    cnt += 1
    file_write_obj.writelines(var)
    file_write_obj.write('\n')
    if cnt % 100000 == 0:
        print('{}/{}'.format(cnt, all_len))

print('Valid Done')


'''
all_len = len(write_out)
print('All len:', all_len)
file_write_obj = open("relation_all.txt", 'a+', encoding='utf-8')
cnt = 0
for var in write_out:
    cnt += 1
    file_write_obj.writelines(var)
    file_write_obj.write('\n')
    if cnt % 100000 == 0:
        print('{}/{}'.format(cnt, all_len))

print('Done')
'''