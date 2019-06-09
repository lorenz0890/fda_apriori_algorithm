#import threading
#import os
#from dotenv import load_dotenv
#import atexit

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
                    new_item = True
                    for item in L1:
                        if word in item.data:
                            item.support +=1
                            new_item = False
                            break
                    if new_item or len(L1) < 1:
                        L1.append(Item([word], 1))
        return L1

    def generate_candidates(self, Ck_1, absolute_min_support, k):
        Ck = []
        vals = []
        for i in range(len(Ck_1)):
            vals = vals + Ck_1[i].data

        vals = list(set(vals)) # make entries unique
        for comb in itertools.combinations(vals, k): #create permutations of length k
            new_comb = list(comb)
            new_item = Item(new_comb, 0)
            for item in Ck_1:
                if set(item.data).issubset(set(new_comb)): #needs some work
                    if item.support >= absolute_min_support: # use a priori information for pruning
                        if new_item not in Ck:
                            Ck.append(new_item)

        for i in range(len(Ck)):
            Ck[i].support = self.calc_support(Ck[i])

        return Ck

    def calc_support(self, item):
        item.support = 0
        for line in self.data:
            if set(item.data).issubset(set(line)):
                item.support +=1
        return item.support

class Item:
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
        #Initialize
        transactions_table = Apriori('movies.txt')
        k=1
        absolute_min_support = 493
        L = transactions_table.find_L1()

        #Write results for a) and b)
        create_output(L, 'oneItems.txt', 'w')
        #create_output(L, 'patterns.txt', 'w')

        # Array to store results in-memory for c)
        results = []

        #Start algorithm, find all combinations in data with specified absolute minimum support
        while len(L) > 0:
            Ck = transactions_table.generate_candidates(L, absolute_min_support, k)
            L = list(filter(lambda item: item.support >= absolute_min_support, Ck))
            # Append more results for b)
            if k == 1:
                create_output(L, 'patterns.txt', 'w')
            else:
                create_output(L, 'patterns.txt', 'a')
            results = results + L
            k += 1


        #Now on to c)
        user_favorites = ['The Shape of Water', 'Three Billboards Outside Ebbing, Missouri']
        user_item = Item(user_favorites, 0)
        user_item.support = transactions_table.calc_support(user_item)

        #calc confidence for items
        confidences = []
        for i, item in enumerate(results):
            if set(user_item.data).issubset(item.data):
                confidences.append([i, item.support/user_item.support])

        for elem in confidences:
            print('Recommended movies: {}'.format(set(results[elem[0]].data).difference(set(user_item.data))))
            print('Confidence for above movies: {}\n'.format(elem[1]))
    except Exception as e:
        print(e)
    exit()
