"""
================
SQLite3 Provider
================
"""
import os.path
import sqlite3

class DBProvider(object):
    """
    SQLite3 powered provider
    """
    def __init__(self):
        self.db = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'example.db'))
        
    def __del__(self):
        self.db.close()
    
    def get_random_user(self):
        """
        Gets a random user from the provider

        :returns: Dictionary
        """
        c = self.db.cursor()
        c.execute('''SELECT username, password, fullname FROM users
                     WHERE rowid >= (abs(random()) % (SELECT max(rowid) FROM users))
                     LIMIT 1''')
        r = c.fetchone()
        return {"username": r[0], "password": r[1], "fullname": r[2]}