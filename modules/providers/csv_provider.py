"""
============
CSV Provider
============
"""
import csv
import os.path
import random

class CSVProvider(object):
    """
    Provides data for either data driven scripting or as oracles from a csv file

    :params c: name of csv file locates in support/csv directory
    """
    def __init__(self, c):
        """
        :params c: name of csv file locates in support/csv directory
        """
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