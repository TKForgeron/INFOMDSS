import json
import requests


def get_population_il():
    try:
        response = requests.get("https://apis.cbs.gov.il/series/data/list?id=3763&startperiod=01-2021&format=json&download=false&lang=en")
        country_population = json.loads(response.content)['DataSet']['Series'][0]['obs'][0]['Value'] * 1000
    except:
        country_population = 9217000
    
    return country_population

def get_population_nsw():
    
    try:
        response = requests.get("https://stat.data.abs.gov.au/sdmx-json/data/ERP_QUARTERLY/1.1.3.TT.Q/all?startTime=2021-Q1")
        observations = json.loads(response.content)['dataSets'][0]['series']["0:0:0:0:0"]['observations']
        latest_observation_key = sorted(observations.keys())[-1]
        country_population = observations[latest_observation_key][0]
    except:
        country_population = 8176369
    
    return country_population

def get_population_nl():
    try:
        response = requests.get("https://opendata.cbs.nl/ODataApi/odata/37296ned/TypedDataSet")
        country_population = json.loads(response.content)['value'][-1]['TotaleBevolking_1']
    except:
        country_population = 17183583
    
    return country_population


