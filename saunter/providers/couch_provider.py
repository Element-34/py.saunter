import ConfigParser
import couchdb.client
import random
import socket
import saunter.ConfigWrapper
from saunter.exceptions import ProviderException

# as will this
class CouchProvider(object):
    def __init__(self, database):
        cf = saunter.ConfigWrapper.ConfigWrapper()

        # read url from the config
        if "couchdb" in cf and "url" in cf["couch"]
            url = cf["saunter"]["couchdb"]["url"]
        else:
            url  = None

        # make sure we can connect to the server
        server = couchdb.client.Server(url=url)
        try:
            server.version()
        except socket.error:
            raise ProviderException('couch server not found at %s' % url)

        # check that the database is in the server
        if database not in server:
            raise ProviderException('database "%s" does not exist' % database)
        self.database = server[database]

# this will live per-project in $saunter_root/lib/providers
# class MySubclassedCouchProvider(CouchProvider):
#     def __init__(self, database):
#         super(MySubclassedCouchProvider, self).__init__(database)

#     def random_user(self):
#         map_fun = '''function(doc) {
#             emit(doc.username, null);
#         }'''
#         all_users = [user.id for user in self.database.query(map_fun=map_fun)]
#         random_user_id = random.choice(all_users)
#         return self.database.get(random_user_id)

#     def random_admin_user(self):
#         map_fun = '''function(doc) {
#             if (doc.role == 'admin')
#                 emit(doc.username, null);
#         }'''
#         all_users = [user.id for user in self.database.query(map_fun=map_fun)]
#         random_user_id = random.choice(all_users)
#         return self.database.get(random_user_id)

# for when I figure out how to test this stuff

# if __name__ == '__main__':
#     # in a py.saunter context, this is stored in the config
#     config = ConfigParser.ConfigParser()
#     config.add_section('couchdb')
#     config.set('couchdb', 'url', 'http://localhost:5984/')

#     c = MySubclassedCouchProvider('people')

#     # records from couchdb are 'just' dictionaries
#     random_user = c.random_user()
#     print(random_user['username'])

#     random_admin_user = c.random_admin_user()
#     print(random_admin_user['username'])