import redis
import pymongo
from bson.objectid import ObjectId
import neo4j
from time import sleep
from elasticsearch import Elasticsearch, helpers

import psycopg2

class Mongo:
    def __init__(self):
        self.__client = pymongo.MongoClient("mongodb://kirill:111@localhost:27017/")
        self.__db = self.__client["university"]
    
    def getDbInstance(self):
        return self.__db

class Neo:
    def __init__(self):
        self.__url = "bolt://localhost:7687"
        self.__dr = neo4j.GraphDatabase.driver(
            self.__url, auth=neo4j.basic_auth("neo4j", "111")
        )
        self.__session = self.__dr.session()
    
    def getDbInstance(self):
        return self.__session

class Elastic:
    def __init__(self):
        self.__es = Elasticsearch('http://elastic:111111@localhost:9200')
    
    def getDbInstance(self):
        return self.__es

class Postgres:
    def __init__(self):
        self.__database_name = "university"
        self.__user_name = "kirill"
        self.__password = "111"
        self.__host_ip = "127.0.0.1"
        self.__host_port ="5432"

        self.__connection = psycopg2.connect(
            database = self.__database_name,
            user = self.__user_name,
            password = self.__password,
            host = self.__host_ip,
            port = self.__host_port
        )
        self.__connection.autocommit = True
        self.__cursor = self.__connection.cursor()
    
    def getDbInstance(self):
        return self.__cursor

class Redis:
    def __init__(self):
        self.__db = redis.Redis(host="localhost", port=6379, db=2)
    
    def getDbInstance(self):
        return self.__db


# start coding...

# redis = Redis()
# mongo = Mongo()
# postg = Postgres()
# neo4j = Neo()
# elast = Elastic()

# query = '''{
#   "query" : {
#     "bool" : {
#       "must" : {
#          "term" : {
#             "material": "Перед"
#          }
#       }
#     }
#   }
# }'''

# es = elast.getDbInstance()
# results = es.search(index="lessons")
# print(results)