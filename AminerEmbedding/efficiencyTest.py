# Name: efficiencyTest
# Author: Reacubeth
# Time: 2020/4/26 12:55
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

# Name: vec_sim
# Author: Reacubeth
# Time: 2020/4/11 13:45
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import random
import time


def cos_sim(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0

    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2

    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)


class EmbeddingModel:
    wv = None

    def read_vec(self, vec_src):
        start = time.time()
        self.wv = {}

        f = open(vec_src, 'r', encoding="utf-8")
        line = f.readline()
        count = 0
        while line:
            count += 1
            if count % 10000 == 9999:
                print('Loading embedding (' + str(count + 1) + ') ......')
            # if count == 100000: break
            line = line.split("\t")
            if 'authorID' not in line[0]:
                line = f.readline()
                continue
            curList = []
            for i in range(1, len(line)):
                curList.append(float(line[i]))
            self.wv[line[0]] = curList
            line = f.readline()

        f.close()
        print('Embedding reading costs %.2fs.' % (time.time() - start))

    def test(self, total):
        start = time.time()
        top_num = total
        vec = self.wv['authorID1347783']
        cur_entity = []
        cur_sim = []
        cnt = 0
        for key, value in self.wv.items():
            sim = cos_sim(vec, value)
            cur_entity.append(key)
            cur_sim.append(sim)

            p = len(cur_entity) - 1
            if p <= 0:
                cur_entity.append(key)
                cur_sim.append(sim)
                continue

            while p >= 0:
                if sim < cur_sim[p]:
                    cur_entity.insert(p + 1, key)
                    cur_sim.insert(p + 1, sim)
                    break
                if p == 0:
                    cur_entity.insert(p, key)
                    cur_sim.insert(p, sim)
                    break
                p -= 1
            if len(cur_entity) > top_num:
                cur_entity = cur_entity[:top_num]
                cur_sim = cur_sim[:top_num]

            cnt += 1
            if cnt == total:
                break

        res = {}
        vis = set()
        top_num -= 1
        for t in range(top_num):
            max_sim = -9999999
            max_item = ''
            for i in range(len(cur_entity)):
                if cur_entity[i] in vis:
                    continue
                if cur_sim[i] > max_sim:
                    max_sim = cur_sim[i]
                    max_item = cur_entity[i]

            res[max_item] = max_sim
            vis.add(max_item)
        print(total, ':\t', time.time() - start)

        return res


emb_model = EmbeddingModel()
emb_model.read_vec('D:/MyProject/AcaFinder/toolkit/embedding/entity_embeddings.tsv')

num_ls = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
for i in num_ls:
    print('-----------------------')
    res = emb_model.test(i)
