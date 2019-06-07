#import threading
#import os
#from dotenv import load_dotenv
#import atexit
import numpy as np



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

    def generate_candidates(self, Ck_1, min_support): #needs some work, doesnt calc new sets properly
        Ck = []
        for i in range(len(Ck_1)):
            for j in range(i+1, len(Ck_1)):
                if Ck_1[i].support >= min_support: # pruning using a proiri property
                    for elem in Ck_1[j].data:
                        if elem not in Ck_1[i].data:
                            new_data = list(Ck_1[i].data)
                            new_data.append(elem)
                            Ck.append(Item(new_data, 0))

                if Ck_1[j].support >= min_support:
                    for elem in Ck_1[i].data:
                        if elem not in Ck_1[j].data:
                            new_data = list(Ck_1[j].data)
                            new_data.append(elem)
                            Ck.append(Item(new_data, 0))

        return Ck

    def calc_support(self, item):
        item.support = 0
        for line in self.data:
            subset = True
            for word in item.data:
                if word not  in line:
                    subset = False
            if subset:
                item.support +=1
        return item.support

class Item:
    def __init__(self, data, support):
        self.data = data
        self.support = support

if __name__ == '__main__':
    try:
        transactions_table = Apriori('movies.txt')
        #Initialize finding L1
        L = transactions_table.find_L1()
        k=1
        min_support = 1500
        while len(L) > 0:
            Ck = transactions_table.generate_candidates(L, min_support)
            print(len(Ck))
            for j in range(len(Ck)):
                Ck[j].support = transactions_table.calc_support(Ck[j])
            L = list(filter(lambda item: item.support > min_support, Ck))
            L = list(dict.fromkeys(L))
            for item in L:
                print(item.data)
                print(item.support)
            k+=1
            print("ASD")
            print(len(L))

    except Exception as e:
        print(e)
    exit()