from kafka import KafkaConsumer
from pymongo import MongoClient
import json

TOPIC_CAF         = 'postgrest.mirea.cafedra'
TOPIC_INS         = 'postgrest.mirea.institutions'
TOPIC_SPE         = 'postgrest.mirea.speciality'
TOPIC_COU         = 'postgrest.mirea.course'
MONGO_CONNECT_CFG = "mongodb://mongo:mongo@mongo:27017"
MONGO_DB          = 'university'
BROKER_HOST       = 'broker:29092'

class Cafedra:
    def __init__(self, db):
        self.inst = db["institutions"]

    def insert(self, i_id, c_code, c_title):
        p_o = {"$push" : {"cafedras" : {"code" : c_code, "title" : c_title}}}
        self.inst.update_one({"id" : i_id}, p_o)

    # one
    def delete(self, i_id, c_code):
        p_o = {"$pull" : {"cafedras" : {"code" : c_code}}}
        self.inst.update_one({"id" : i_id, "cafedras.code" : c_code}, p_o)

    # many
    def delete(self, c_code):
        p_o = {"$pull" : {"cafedras" : {"code" : c_code}}}
        self.inst.update_one({"cafedras.code" : code}, p_o)

    def update(self, i_id, c_code, c_title):
        a_filter = [{"caf.code" : c_code}]
        s_o = {"$set" : {"cafedras.$[caf].title" : c_title}}
        inst.update_one({"id" : i_id}, s_o, array_filters=a_filter)

class Specialty:
    def __init__(self, db):
        self.inst = db["institutions"]

    def insert(self, c_code, s_code, s_title):
        a_filter = [{"caf.code":c_code}]
        p_o = {"$push" : {"cafedras.$[caf].specialties" : {
                            "code" : s_code, "title" : s_title}}}
        # if needed => update_many
        self.inst.update_one({"cafedras.code" : c_code}, p_o, array_filters=a_filter)

    # one
    def delete(self, c_code, s_code):
        p_o = {"$pull" : {"cafedras.$.specialties" : {"code" : s_code}}}
        self.inst.update_one({"cafedras.code" : c_code,
                              "cafedras.specialties.code" : s_code}, p_o)

    # many
    def delete(self, s_code):
        p_o = {"$pull" : {"cafedras.$.specialties" : {"code" : s_code}}}
        self.inst.update_one({"cafedras.specialties.code" : s_code}, p_o)

    def update(self, s_code, s_title):
        a_filter = [{"spec.code":s_code}]
        s_o = {"$set":{"cafedras.$.specialties.$[spec].title":s_title}}
        inst.update_one({"cafedras.specialties.code":s_code}, s_o, array_filters=a_filter)

def process_institutions(json_data, db):
    if json_data['after'] != None:
        inst  = db["institutions"]
        title = json_data['after']['title']
        id    = json_data['after']['id']
        if json_data['op'] == 'c':
            inst.insert_one({"id" : id, "title" : title})
        if json_data['op'] == 'u':
            inst.update_one({"id" : id}, {"$set": {"title" : title}})
    if json_data['op'] == 'd' and json_data['before'] != None:
        inst.delete_one({"id" : json_data['before']['id']})

def process_cafedras(json_data, db):
    caf = Cafedra(db)
    if json_data['after'] != None:
        title = json_data['after']['title']
        code  = json_data['after']['code']
        i_id  = json_data['after']['institution_id']
        if json_data['op'] == 'c':
            caf.insert(i_id, code, title)
        if json_data['op'] == 'u' and json_data['before'] != None:
            i_id_b = json_data['before']['institution_id'] 
            if i_id_b != i_id:
                caf.insert(i_id, code, title)  
                caf.delete(i_id_b, code)
            else:
                caf.update(i_id, code, title)
    if json_data['op'] == 'd' and json_data['before'] != None:
        code = json_data['before']['code']
        caf.delete(code)

def process_specialties(json_data, db):
    spec = Specialty(db)
    if json_data['after'] != None:
        title  = json_data['after']['title']
        code   = json_data['after']['code']
        c_code = json_data['after']['cafedra_code']
        if json_data['op'] == 'c':
            spec.insert(c_code, code, title)
        if json_data['op'] == 'u' and json_data['before'] != None:
            c_code_b = json_data['before']['cafedra_code']
            if c_code != c_code_b:
                spec.insert(c_code, code, title)
                spec.delete(c_code_b, code)
            else:
                spec.update(code, title)
    if json_data['op'] == 'd' and json_data['before'] != None:
        code = json_data['before']['code']
        spec.delete(code)
    
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
        #test
        print(msg)
        record = json.loads(msg.value)
        try:
            if msg.topic == TOPIC_CAF:
                process_cafedras(record, db)
            if msg.topic == TOPIC_COU:
                process_courses(record, db)
            if msg.topic == TOPIC_INS:
                process_institutions(record, db)
            if msg.topic == TOPIC_SPE:
                process_specialties(record, db)
        except:
            print("Could't exec op '{}' into {}".format(msg.value['op'], msg.topic))
            print(json_data)

        break;
