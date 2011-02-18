import csv
import os.path
import random

class CSVProvider(object):
    def __init__(self, c):
        f = os.path.join(os.path.dirname(__file__), '..', '..', 'support', 'csv', c)
        self.data = csv.DictReader(open(f, 'r'))
        
    def randomRow(self):
        """
        Gets a random row from the provider

        :returns: List
        """
        l = []
        for row in self.data:
            l.append(row)
        return random.choice(l)