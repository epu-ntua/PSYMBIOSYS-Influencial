import requests
import pprint
import json

def parse_anlzer_weeks(topics, accounts, from_timestamp, until_timestamp ):

    resource = 'http://83.212.114.237:8000/api/project/1/report/dailyhistogram?topics='



    for topic in topics:
        resource =  resource + topic +","

    resource = resource[:-1]

    resource = resource + "&accounts="
    for account in accounts:
        resource =  resource +"twitter:"+ account['username'] +","

    resource = resource[:-1]


    resource = resource + "&from_timestamp="+str(from_timestamp)
    resource = resource + "&until_timestamp=" +str(until_timestamp)


    result = requests.get(url=resource)

    print result.url

    return result.json()['facets']


def top_topics(size):
    resource = 'http://83.212.114.237:8000/api/project/1/report/popular_hashtags?size='+str(size)
    result = requests.get(url=resource)
    terms = []
    for term in result.json()['facets']['terms']['terms']:
        terms.append(str(term['term']))

    return terms
# pprint.pprint(parse_anlzer_weeks(topics=['dress','dior','gold'],accounts=[{'username':'Wedding_Planz'},{'username':'mpetyx'}],from_timestamp='1451899408484',until_timestamp='1454491408484'))
# pprint.pprint(top_topics(40))