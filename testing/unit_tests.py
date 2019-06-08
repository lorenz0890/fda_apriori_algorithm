import unittest
import apriori as a
import numpy as np

class TestKummer(unittest.TestCase):

    def test_generate_candidates(self):
        transactions_table = a.Apriori('../movies.txt')
        # Initialize finding L1
        L = transactions_table.find_L1()
        k = 1
        min_support = 500

        Ck = transactions_table.generate_candidates(L, min_support, 2)

        Ck = list(filter(lambda item: item.support > min_support, Ck))

        Ck = transactions_table.generate_candidates(Ck, min_support, 3)

        Ck = list(filter(lambda item: item.support > min_support, Ck))
        print(len(Ck))
        for item in Ck:
            print(item.data)
            print(item.support)

    def test_generate_L1(self):
        transactions_table = a.Apriori('../movies.txt')
        # Initialize finding L1
        L = transactions_table.find_L1()
        for item in L:
            print(item.data)
            print(item.support)