from pymongo import MongoClient
from random import randint
from incidents import list_alerts_violations ## Incidents module most in same path as this file.
# Replace these with your Connection details
MONGO_HOST = "192.168.1.20" 
MONGO_PORT = 27017
MONGO_DB = "newrelic"
MONGO_USER = "admin"
MONGO_PASS = "" ## Give mongo admin userpassword

URI = "mongodb://{}:{}@{}:{}/{}".format(MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB)
CLIENT = MongoClient(URI)
# DB Name in Mongo is newrelic
DB = CLIENT.newrelic
# list_alerts_violations returns json object from newrelic API
LIST_ALERTS = list_alerts_violations(start_date="2020-05-25T16:55:00+00:00",end_date="2020-05-28T16:56:00+00:00",only_open="true")

# No-data return if the No alerts in specified dates.
# Get the max _id from all_db_alerts table, increase by 1 for next row.
if 'No-data' not in LIST_ALERTS:
    RESULT_SET={}
    MAX_ID_VALUE=0
    RESULT_SET=DB.all_db_alerts.find({},({"_id":1})).sort("_id",-1).limit(1)
    if RESULT_SET:
        for DOCUMENT in RESULT_SET:
             MAX_ID_VALUE = DOCUMENT['_id']
             
           
      
    for index,itr in enumerate(LIST_ALERTS['violations'],1):
        INCIDENT_DETAILS = {
        "_id" : index + MAX_ID_VALUE,
        'alrert_id' :itr['id'],
        'incident_details' : itr['links']['incident_id'],
        'label' : itr['label'],
        'opened_at': itr['opened_at'],
        'entity_name': itr['entity']['name']
        }

        WITH_OUT_INCIDENT_DETAILS = {
        'alrert_id' :itr['id'],
        'incident_details' : itr['links']['incident_id'],
        'label' : itr['label'],
        'opened_at': itr['opened_at'],
        'entity_name': itr['entity']['name']
        }

        # If the record alredy exits, update the details
        # If record not exits then insert record with new _id
        if DB.all_db_alerts.find({'alrert_id': itr['id']}).count() > 0:
            result=DB.all_db_alerts.update(WITH_OUT_INCIDENT_DETAILS,WITH_OUT_INCIDENT_DETAILS,upsert= True)
        else:
            result=DB.all_db_alerts.update(INCIDENT_DETAILS,INCIDENT_DETAILS,upsert= True)
