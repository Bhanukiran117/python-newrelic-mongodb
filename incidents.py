import requests
import json

 
AUTH_TOK = 'NRAA-'  # For Put requests you have get admin API Token, else you get permission denied.
HEADERS = {
    'X-Api-Key': '{0}'.format(AUTH_TOK),
    'Content-type': 'application/json',
}

incident_data_dict = {}
#list_alerts_violations ={}



def get_incident(incident_number):
    ivars = {}
    ivars['base_url'] = "https://api.newrelic.com/v2/alerts_incidents"
    ivars['incident_number'] = incident_number
    results = requests.get(
    '{base_url}/{incident_number}.json'.format(**ivars),
    headers=HEADERS
    )
    return results.json() if results.status_code == 200 else "{'No-data':'Not found'}"
   
def list_alerts_violations(start_date,end_date,only_open):
    ivars = {}
    ivars['base_url'] = "https://api.newrelic.com/v2/alerts_violations.json"
    var_params = {
        "start_date" : start_date,
        "end_date" : end_date,
        "only_open" : only_open
    }
    results = requests.get(
    '{base_url}'.format(**ivars),
    headers=HEADERS,
    params=var_params
    )
    return results.json() if results.status_code == 200 else "{'No-data':'Not found'}"

def post_incident_ack(incident_number):
    ivars = {}
    ivars['base_url'] = "https://api.newrelic.com/v2/alerts_incidents"
    ivars['incident_number'] = incident_number
    results = requests.put(
    '{base_url}/{incident_number}/acknowledge.json'.format(**ivars),
    headers=HEADERS
    )
    return "Successful Ack" if results.status_code == 200 else "Failure Ack"


def post_incident_close(incident_number):
    ivars = {}
    ivars['base_url'] = "https://api.newrelic.com/v2/alerts_incidents"
    ivars['incident_number'] = incident_number
    results = requests.put(
    '{base_url}/{incident_number}/close.json'.format(**ivars),
    headers=HEADERS
    )
    return "Close Successful" if results.status_code == 200 else "Close Successful"
    
