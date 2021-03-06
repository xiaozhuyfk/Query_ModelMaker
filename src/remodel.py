# remodel.py
# Hongyu Li

# This module is to rank the models by a score we calculate in certain standards

import os, re, rw

class Remodel(object):
    def __init__(self, m, coeff_fvq, coeff_num, coeff_key, res_dir, dict_dir):
        self.m = m
        self.coeff_fvq = coeff_fvq
        self.coeff_num = coeff_num
        self.coeff_key = coeff_key
        self.res_dir = res_dir
        self.dict_dir = dict_dir
        self.dic = {}
        self.dictionary = set()
        self.dic_list = []

    # init the high frequency words dictionary
    def init_dict(self):
        words = rw.readFile(self.dict_dir).split('\n')[0:-1]
        for word in words:
            self.dictionary.add(word)

    # evaluate the score of the given model by different coefficients
    def evaluate(self, key, dic):
        score = 0
        fvq, num = dic[key]
        fvq_l, num_l = zip(*dic.values())
        max_fvq = max(fvq_l)
        max_num = max(num_l)
        ratio_fvq = float(fvq)/max_fvq
        ratio_num = float(num)/max_num
        score += ((ratio_fvq * self.coeff_fvq) + (ratio_num * self.coeff_num))
        count = 0
        for word in self.dictionary:
            if word in key:
                count += 1
        score += (count * self.coeff_key)
        return (score,dic[key])

    # Same list of models, but in a new ranking
    # Write the result of remodeling in the result directory
    def filter(self,dic,filename):
        d = {}
        for key in dic:
            d[key] = self.evaluate(key,dic)
        content = ""
        path = self.res_dir + '/' + filename + '.txt'
        result = sorted(d.items(), key = lambda d: d[1][0])[::-1]
        for query,score in result:
            line = (query + '\t' + str(score) + '\n')
            content += line
        rw.writeFile(path,content)
        return (d,result)

    # Categorize the models
    def classification(self):
        for category in self.m.type_dic:
            self.filter(self.m.type_dic[category],category)

    # the main funciton
    def run(self):
        self.init_dict()
        self.dic, self.dic_list = self.filter(self.m.dic,'general')
        self.classification()
            
        

    

