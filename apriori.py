#import threading
#import os
#from dotenv import load_dotenv
#import atexit
import numpy as np
import itertools


class Apriori:

    def __init__(self, data_path):
        self.supports = {}
        self.data = []
        self.data_path = data_path
        self.data = self.__load_data(data_path)
        self.data = self.__clean_data(self.data)


    def __load_data(self, data_path):
        file = open(data_path)
        data = None
        try:
            data = file.readlines()
        except Exception as e:
            file.close()
        file.close()
        return data

    def __clean_data(self,data):
        for i in range(len(data)):
            data[i] = data[i].strip()
            data[i] = data[i].split(';')
        return data

    def find_L1(self):
        L1 = []
        for line in self.data:
            for word in line:
                if len(word)>0:
                    new_node = True
                    for node in L1:
                        if word in node.data:
                            node.support +=1
                            new_node = False
                            break
                    if new_node or len(L1) < 1:
                        L1.append(Node([word], 1))
        return L1

    def generate_candidates(self, Ck_1, absolute_min_support, k):
        Ck = []
        vals = []
        for i in range(len(Ck_1)):
            vals = vals + Ck_1[i].data

        vals = list(set(vals)) # make entries unique
        for comb in itertools.combinations(vals, k): #create permutations of length k
            new_comb = list(comb)
            new_node = Node(new_comb, 0)
            for node in Ck_1:
                if set(node.data).issubset(set(new_comb)):
                    if node.support >= absolute_min_support: # use a priori information for pruning
                        if new_node not in Ck:
                            Ck.append(new_node)

        for i in range(len(Ck)):
            Ck[i].support = self.__calc_support(Ck[i])

        return Ck

    def __calc_support(self, item):
        item.support = 0
        for line in self.data:
            if set(item.data).issubset(set(line)):
                item.support +=1
        return item.support

class Node:
    def __init__(self, data, support):
        self.data = data
        self.support = support

def create_output(L, file_name, options):
    file = open(file_name, options)
    for item in L:
        movie_string = item.data[0]
        for i, movie in enumerate(item.data):
            if i > 0:
                movie_string += ';'
                movie_string+=movie
        movie_string += '\n'
        file.write("{}:{}".format(item.support,movie_string))
    file.close()


if __name__ == '__main__':
    try:
        transactions_table = Apriori('movies.txt')
        k=1
        absolute_min_support = 493
        L = transactions_table.find_L1()
        create_output(L, 'oneItem.txt', 'w')
        create_output(L, 'patterns.txt', 'w')
        while len(L) > 0:
            Ck = transactions_table.generate_candidates(L, absolute_min_support, k)
            L = list(filter(lambda item: item.support >= absolute_min_support, Ck))
            k+=1
            create_output(L, 'patterns.txt', 'a')

    except Exception as e:
        print(e)
    exit()
