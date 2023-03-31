from kafka import KafkaConsumer
from pymongo import MongoClient
import json

TOPIC_CAF         = 'dbserverpostgres.public.cafedra'
TOPIC_INS         = 'dbserverpostgres.public.institution'
TOPIC_SPE         = 'dbserverpostgres.public.specialty'
TOPIC_COU         = 'dbserverpostgres.public.course'
MONGO_CONNECT_CFG = "mongodb://mongo:mongo@mongo:27017"
MONGO_DB          = 'university'
BROKER_HOST       = 'broker:29092'

def process_institutions(json_data, db):
    if json_data['after'] != None:
        title = json_data['after']['title']
        id = json_data['after']['id']
        if json_data['op'] == 'c':
            try:
                db["institutions"].insert_one({"id" : id, "title" : title})
            except:
                print("Could not insert (c) into Instituions")
        if json_data['op'] == 'u':
            try:
                db["institutions"].update_one({"id" : id}, {"$set": {"title" : title}})
            except:
                print("Could not insert (u) into Instituions")
    if json_data['op'] == 'd' and json_data['before'] != None:
        id = json_data['before']['id']
        try:
            db["institutions"].delete_one({"id" : id})
        except:
            print("Could not delete from Instituions")

def process_cafedras(json_data, db):
    if json_data['after'] != None:
        id = json_data['after']['institutionid']
        title = json_data['after']['title']
        code = json_data['after']['code']
        if json_data['op'] == 'c':
            push_obj = {"$push" : {"cafedras" : {"code" : code, "title" : title}}}
            try:
                db["institutions"].update_one({"id" : id}, push_obj)
            except:
                print("Could not insert (c) into Inst.Cafedras")
        if json_data['op'] == 'u':
            arr_filter = [{"caf.code":code}]
            set_obj = {"$set":{"cafedras.$[caf].title":title}}
            try:
                db["institutions"].update_one(
                        {"id":id}, set_obj, array_filters=arr_filter
                )
            except:
                print("Could not insert (u) into Inst.Cafedras")
    if json_data['op'] == 'd' and json_data['before'] != None:
        code = json_data['before']['code']
        pull_obj = {"$pull" : {"cafedras" : {"code" : code}}}
        try:
            db["institutions"].update_one({"cafedras.code" : code}, pull_obj)
        except:
            print("Could not delete from Inst.Cafedras")

def process_specialties(json_data, db):
    if json_data['after'] != None:
        caf_code = json_data['after']['cafedracode']
        title = json_data['after']['title']
        code = json_data['after']['code']
        if json_data['op'] == 'c':
            arr_filter = [{"caf.code":caf_code}]
            push_obj = {"$push" : {"cafedras.$[caf].specialties" : {"code" : code, "title" : title}}}
            try:
                db["institutions"].update_one(
                        {"cafedras.code" : caf_code}, push_obj, array_filters=arr_filter
                )
            except:
                print("Could not insert (c) into Inst.Cafs.Specs")
        if json_data['op'] == 'u':
            arr_filter = [{"spec.code":code}]
            set_obj = {"$set":{"cafedras.$.specialties.$[spec].title":title}}
            try:
                db["institutions"].update_one(
                        {"cafedras.specialties.code":code}, set_obj, array_filters=arr_filter
                )
            except:
                print("Could not insert (u) into Inst.Cafs.Specs")
    if json_data['op'] == 'd' and json_data['before'] != None:
        code = json_data['before']['code']
        pull_obj = {"$pull" : {"cafedras.$.specialties" : {"code" : code}}}
        try:
            db["institutions"].update_one({"cafedras.specialties.code" : code}, pull_obj)
        except:
            print("Could not delete from Inst.Cafs.Specs")

def process_courses(json_data, db):
    print(json_data)
    if json_data['after'] != None:
        id = json_data['after']['id']
        caf_code = json_data['after']['cafcode']
        title = json_data['after']['title']
        if json_data['op'] == 'c':
            arr_filter = [{"caf.code": caf_code}]
            push_obj = {"$push" : {"cafedras.$[caf].courses" : {"id" : id, "title" : title}}}
            try:
                db["institutions"].update_one({"cafedras.code" : caf_code}, push_obj, array_filters=arr_filter)
            except:
                print("Could not insert (c) into Inst.Cafedras.Courses")
        if json_data['op'] == 'u':
            arr_filter = [{"course.id":id}]
            set_obj = {"$set":{"cafedras.$.courses.$[course].title":title}}
            try:
                db["institutions"].update_one(
                        {"cafedras.courses.id":id}, set_obj, array_filters=arr_filter
                )
            except:
                print("Could not insert (u) into Inst.Cafedras.Courses")
    if json_data['op'] == 'd' and json_data['before'] != None:
        id = json_data['before']['id']
        pull_obj = {"$pull" : {"cafedras.$.courses" : {"id" : id}}}
        try:
            db["institutions"].update_one({"cafedras.courses.id" : id}, pull_obj)
        except:
            print("Could not delete from Inst.Cafedras.Courses")

# connect to mongo
try:
   client = MongoClient(MONGO_CONNECT_CFG)
   db = client[MONGO_DB]
except:  
   print("Could not connect to MongoDB")
    
# connect kafka consumer to desired kafka topic	
try:
   consumer = KafkaConsumer(bootstrap_servers=[BROKER_HOST])
   consumer.subscribe([TOPIC_CAF, TOPIC_COU, TOPIC_INS, TOPIC_SPE])
except:  
   print("Could not connect to Kafka")

# processing messages
while True:
    # parse received data from Kafka
    for msg in consumer:
        if msg.value == None:
            continue;
        record = json.loads(msg.value)
        if msg.topic == TOPIC_CAF:
            process_cafedras(record, db)
        if msg.topic == TOPIC_COU:
            process_courses(record, db)
        if msg.topic == TOPIC_INS:
            process_institutions(record, db)
        if msg.topic == TOPIC_SPE:
            process_specialties(record, db)
        break;
