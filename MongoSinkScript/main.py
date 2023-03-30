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
    if json_data['op'] == 'c' and json_data['after'] != None:
        title = json_data['after']['title']
        try:
            db["institutions"].insert_one({"title" : title})
        except:
            print("Could not insert into Instituions")
    print(json_data)

def process_cafedras(json_data, db):

    print(json_data)

def process_specialties(json_data, db):
    print(json_data)

def process_courses(json_data, db):
    print(json_data)

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
