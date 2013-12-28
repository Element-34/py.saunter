# Copyright 2013 Element 34
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
================
mysql_provider
================
"""
import mysql.connector

import saunter.ConfigWrapper


class DBProvider(object):
    """
    MySQL powered provider

    :params db: name of db file located in support/db directory
    """
    def __init__(self, db):
        try:
            cf = saunter.ConfigWrapper.ConfigWrapper()
        except:
            print('ooooo')

        self.mysql = mysql.connector.connect(
            user=cf["saunter"]["mysql"]["user"],
            password=cf["saunter"]["mysql"]["password"],
            host=cf["saunter"]["mysql"]["host"],
            database=cf["saunter"]["mysql"]["database"]
        )

    def __del__(self):
        self.mysql.close()

    # this would sit in the client side implementation

    # def get_random_user(self):
    #     """
    #     Gets a random user from the provider

    #     :returns: Dictionary
    #     """
    #     c = self.db.cursor()
    #     c.execute('''SELECT username, password, fullname FROM users
    #                  WHERE rowid >= (abs(random()) % (SELECT max(rowid) FROM users))
    #                  LIMIT 1''')
    #     r = c.fetchone()
    #     return {"username": r[0], "password": r[1], "fullname": r[2]}
