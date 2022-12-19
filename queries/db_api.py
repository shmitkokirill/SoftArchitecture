import redis
import pymongo
from bson.objectid import ObjectId
import neo4j
from time import sleep
from elasticsearch import Elasticsearch, helpers

from prettytable import PrettyTable
import psycopg2

class Mongo:
    def __init__(self):
        self.__client = pymongo.MongoClient(
            "mongodb://kirill:111@localhost:27017"
        )
        self.__db = self.__client["university"]
    
    def exec_find_query(self, collection_name, find_object):
        collection = self.__db[collection_name]
        return collection.find(find_object)
    
    # 2-nd query
    def get_courseInfo_table(self, course_title):
        # result = course_title + "\n"
        result = PrettyTable()
        result.field_names = [
            "Курс", "Код спец.", "Название спец.", 
            "Код каф.", "Название каф.", "Институт"
        ]

        courses = self.__db["Courses"]
        specs = self.__db["Specialties"]
        cafedras = self.__db["Cafedras"]
        instits = self.__db["Institutions"]

        course = courses.find_one({"Title" : course_title})

        specs_founded = specs.find({"Courses_ids": ObjectId(course['_id'])})

        specs_str = ''
        insts_str = ''
        cafs_str = ''
        for spec in specs_founded:
            caf_finded = cafedras.find({"Specs_ids": ObjectId(spec['_id'])})
            for caf in caf_finded:
                instits_finded = instits.find({"Cafedras_ids" : ObjectId(caf['_id'])})
                for inst in instits_finded:
                    result.add_row(
                        [
                            course_title, 
                            spec['Code'],
                            spec['Title'], 
                            caf['Code'],
                            caf['Title'],
                            inst['Title']
                        ]
                    )
        return result
    
    def getDbInstance(self):
        return self.__db

class Neo:
    def __init__(self):
        self.__url = "bolt://localhost:7687"
        self.__dr = neo4j.GraphDatabase.driver(
            self.__url, auth=neo4j.basic_auth("neo4j", "111")
        )
        self.__session = self.__dr.session()
    
    def exec_query(self, query):
        return self.__session.run(query).values()
    
    def get_groupInfo_by_studs(self, studs_str):
        query = "MATCH (st)-[]->(g:Group)-[]->(s:Specialty)-[]->\
            (c:Cafedra)-[]->(i:Institution) \
                WHERE st.code in [" + studs_str + "] \
                    RETURN \
                        st.code as stud_code, g.code as g_code, \
                            s.code as spec_code, c.code as caf_code, \
                                i.title as i_title"
        return self.__session.run(query).values()

    
    # 2-nd query
    def get_students_count(self, lesson_ids : str, course_title):
        query = "MATCH (l:Lesson)-[]->(c:Course)-[]->\
            (s:Specialty)<-[]-(g:Group)<-[r]-(st:Student)\
                where l.id in [" + lesson_ids + "] and \
                    c.title = '" + course_title + "'\
                        RETURN count(distinct st)"
        return self.__session.run(query).value()

    def get_lessons_ids(self, course_title):
        query = "match (c:Course)<-[]-(l:Lesson) \
            where c.title = '" + course_title + "' return distinct l.id"
        return self.__session.run(query).value()
    
    def get_group_info(self, group : str):
        query = "match (g:Group {code: '" + group + "'})-[]->(s:Specialty)\
            -[]->(c:Cafedra)-[]->(i:Institution) \
                return g.code, s.code, c.code, i.title"
        return self.__session.run(query).values()

    
    def getDbInstance(self):
        return self.__session

class Elastic:
    def __init__(self):
        self.__es = Elasticsearch('http://elastic:111111@localhost:9200')

    # 3-rd query
    def getLessonsByTerm(self, term):
        return self.__es.search(
            index="lessons", 
            body={
                "query": {
                    "bool" : { 
                        "must" : 
                            [{"match": {"material": term}}]
                    }
                }
            }
        )
    
    # 2-nd query
    def getLessonsByTerm_Ids(self, term, ids_list):
        return self.__es.search(
            index="lessons", 
            body={
                "query": {
                    "bool" : { 
                        "must" : 
                            [{"match": {"material": term}}], 
                        "filter" : {
                            "terms" : {"id" : ids_list}
                        }
                    }
                }
            }
        )

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
    
    def get_10_studs(self, start_date, end_date, les_ids):
        query = \
        "SELECT v.studentid, count(*) as cnt \
            FROM TimeTable t, visit v WHERE \
                (t.id = v.tt_id) and \
                    (t.date>'"+start_date+"'::date and t.date<'"+end_date+"'::date) and \
                            t.lessonid in (" + les_ids + ") and \
                                v.isvisited = false \
                                group by v.studentid \
                                    order by cnt desc \
                                    limit 10;"
        self.__cursor.execute(query)
        return self.__cursor.fetchall()
    
    def get_allStuds(self, start_date, end_date, les_ids):
        query = \
    "SELECT v.studentid, count(*) as cnt \
        FROM TimeTable t, visit v WHERE \
            (t.id = v.tt_id) and \
                (t.date>'"+start_date+"'::date and t.date<'"+end_date+"'::date) and \
                        t.lessonid in (" + les_ids + ") \
                            group by v.studentid;"
        self.__cursor.execute(query)
        return self.__cursor.fetchall()
        

    # 2-nd query
    def get_lesIds_by_period_lesIds(self, start_date, end_date, less_ids):
        query = "SELECT distinct t.lessonid FROM TimeTable t WHERE \
            (t.date > '" + start_date + "'::date and \
                t.date < '" + end_date + "'::date) and\
                    t.lessonid in (" + less_ids + ");"
        self.__cursor.execute(query)
        return self.__cursor.fetchall()

    # 3-rd query
    def get_ttIds_by_group(self, start_date, end_date, less_ids, group):
        query = "SELECT t.id FROM TimeTable t WHERE \
            t.groupid = '" + group + "' and \
            (t.date > '" + start_date + "'::date and \
                t.date < '" + end_date + "'::date) and\
                    t.lessonid in (" + less_ids + ");"
        self.__cursor.execute(query)
        return self.__cursor.fetchall()
    
    def get_studHours_table(self, tt_ids : str):
        query = "select studentid, count(*) from visit \
            where tt_id in (" + tt_ids + ") and \
                isvisited = true group by studentid";
        self.__cursor.execute(query)
        return self.__cursor.fetchall()

    
    def getDbInstance(self):
        return self.__cursor

class Redis:
    def __init__(self):
        self.__db = redis.Redis(host="localhost", port=6379)
    
    def get_fio(self, code : str):
        return self.__db.get(code).decode("utf-8")
    
    def getDbInstance(self):
        return self.__db