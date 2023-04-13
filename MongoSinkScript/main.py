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

    def find(self, finded_doc, c_code):
        if finded_doc == None:
            return [] 
        if finded_doc["cafedras"]:
            cafs = finded_doc["cafedras"]
            for caf in cafs:
                if caf["code"] != c_code:
                    continue
                if caf["specialties"]:
                    return caf["specialties"]
        return []

    def insert(self, i_id, c_code, c_title, nested = False):
        if not nested:
            p_o = {"$push" : {"cafedras" : {"code" : c_code, "title" : c_title}}}
            self.inst.update_one({"id" : i_id}, p_o)
        else:
            finded_doc = self.inst.find_one(
                    {"cafedras.code" : c_code},
                    {"cafedras.$" : 1}
            )
            specs = self.find(finded_doc, c_code)
            p_o = {"$push" : 
                   {"cafedras" : 
                    {"code" : c_code, "title" : c_title, "specialties" : specs}}}
            self.inst.update_one({"id" : i_id}, p_o)

    # one
    def delete_one(self, i_id, c_code):
        p_o = {"$pull" : {"cafedras" : {"code" : c_code}}}
        self.inst.update_one({"id" : i_id, "cafedras.code" : c_code}, p_o)

    # many
    def delete(self, c_code):
        p_o = {"$pull" : {"cafedras" : {"code" : c_code}}}
        self.inst.update_one({"cafedras.code" : code}, p_o)

    def update(self, i_id, c_code, c_title):
        a_filter = [{"caf.code" : c_code}]
        s_o = {"$set" : {"cafedras.$[caf].title" : c_title}}
        self.inst.update_one({"id" : i_id}, s_o, array_filters=a_filter)

class Specialty:
    def __init__(self, db):
        self.inst = db["institutions"]

    def find(self, finded_doc, s_code):
        if finded_doc == None:
            return [] 
        if finded_doc["cafedras"][0]                 and \
           finded_doc["cafedras"][0]["specialties"]:
            specs = finded_doc["cafedras"][0]["specialties"]
            for spec in specs:
                if spec["code"] != s_code:
                    continue
                if spec["courses"]:
                    return spec["courses"]
        return []

    def insert(self, c_code, s_code, s_title, nested = False):
        if not nested:
            a_filter = [{"caf.code" : c_code}]
            p_o = {"$push" : 
                   {"cafedras.$[caf].specialties" : 
                    {"code" : s_code, "title" : s_title}}}
            # if needed => update_many
            self.inst.update_one (
                {"cafedras.code" : c_code}, p_o, array_filters=a_filter
            )
        else:
            finded_doc = self.inst.find_one(
                {"cafedras.specialties.code" : s_code},
                {"cafedras.specialties.$" : 1}
            )
            courses = self.find(finded_doc, s_code)
            a_filter = [{"caf.code":c_code}]
            p_o = {"$push" : {"cafedras.$[caf].specialties" : {
                    "code" : s_code, "title" : s_title, "courses": courses}}}
            # if needed => update_many
            self.inst.update_one(
                {"cafedras.code" : c_code}, p_o, array_filters=a_filter
            )

    # one
    def delete_one(self, c_code, s_code):
        a_filter = [{"caf.code" : c_code}]
        p_o = {"$pull" : {"cafedras.$[caf].specialties" : {"code" : s_code}}}
        self.inst.update_one(
            {"cafedras.code" : c_code}, p_o, array_filters=a_filter
        )

    # many
    def delete(self, s_code):
        p_o = {"$pull" : {"cafedras.$.specialties" : {"code" : s_code}}}
        self.inst.update_one({"cafedras.specialties.code" : s_code}, p_o)

    def update(self, s_code, s_title):
        a_filter = [{"spec.code":s_code}]
        s_o = {"$set":{"cafedras.$.specialties.$[spec].title":s_title}}
        self.inst.update_one(
            {"cafedras.specialties.code":s_code}, s_o, array_filters=a_filter
        )

class Course:
    def __init__(self, db):
        self.inst = db["institutions"]

    def insert(self, s_code, c_id, c_title):
        a_filter = [{"spec.code" : s_code}]
        p_o = {"$push" : 
               {"cafedras.$.specialties.$[spec].courses" : 
                {"id" : c_id, "title" : c_title}}}
        # if needed => update_many
        self.inst.update_one(
            {"cafedras.specialties.code" : s_code}, p_o, array_filters=a_filter
        )

    # one
    def delete_one(self, s_code, c_id):
        a_filter = [{"spec.code" : s_code}]
        p_o = {"$pull" : 
               {"cafedras.$.specialties.$[spec].courses" : {"id" : c_id}}}
        self.inst.update_one(
            {"cafedras.specialties.code" : s_code}, p_o, array_filters=a_filter
        )

    # many
    def delete(self, c_id):
        a_filter = [{"cour.courses.id" : 1}]
        p_o = {"$pull" : 
               {"cafedras.$.specialties.$[cour].courses" : {"id" : c_id}}}
        self.inst.update_one(
            {"cafedras.specialties.courses.id" : c_id}, p_o, array_filters = a_filter
        )

    def update(self, c_id, c_title):
        a_filter = [{"spec.code":s_code}]
        s_o = {"$set":{"cafedras.$.specialties.$[spec].courses.title" : c_title}}
        self.inst.update_one(
            {"cafedras.specialties.courses.id" : c_id}, s_o, array_filters=a_filter
        )

def process_institutions(json_data, db):
    inst = db["institutions"]
    if json_data['after'] != None:
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
                caf.insert(i_id, code, title, True)  
                caf.delete_one(i_id_b, code)
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
                spec.insert(c_code, code, title, True)
                spec.delete_one(c_code_b, code)
            else:
                spec.update(code, title)
    if json_data['op'] == 'd' and json_data['before'] != None:
        code = json_data['before']['code']
        spec.delete(code)
    
def process_courses(json_data, db):
    c = Course(db)
    if json_data['after'] != None:
        title  = json_data['after']['title']
        c_id   = json_data['after']['id']
        s_code = json_data['after']['spec_code']
        if json_data['op'] == 'c':
            c.insert(s_code, c_id, title)
        if json_data['op'] == 'u' and json_data['before'] != None:
            s_code_b = json_data['before']['spec_code']
            if s_code != s_code_b:
                c.insert(s_code, c_id, title)
                c.delete_one(s_code_b, c_id)
            else:
                c.update(c_id, title)
    if json_data['op'] == 'd' and json_data['before'] != None:
        c_id = json_data['before']['id']
        c.delete(c_id)

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
