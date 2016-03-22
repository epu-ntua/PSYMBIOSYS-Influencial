# -*- coding: utf-8 -*-

__author__ = 'Michael'

from algorithms.data_samples.evmorfia_final import temp
from tweetfluence.models import Influencer

def influencers(lista):
    people = []

    for doc in lista:
        name = doc['doc']['user_screen_name']
        name = name.replace('twitter:','')
        people.append(name)
        if doc['doc']['entities']['user_mentions']:
            for person in doc['doc']['entities']['user_mentions']:
                people.append(person['screen_name'])


    return list(set(people))

def prepare_rank( topic):
    people = influencers(temp)
    lista = temp
    results = []
    for doc in lista:
        if not topic in doc['doc']['text'].lower():
            continue
        for person in people:
            if person in doc['doc']['text'].replace('twitter:', ''):
                if person == doc['doc']['user_screen_name'].replace('twitter:', ''):
                    continue
                else:

                    try:
                        connection = [ Influencer.objects.get(twitter_username=doc['doc']['user_screen_name'].replace('twitter:', '')).id,Influencer.objects.get(twitter_username=person).id]
                    except:
                        continue
                    results.append( {
                        "connection":connection,
                        "topic-name":topic
                        }
                    )

    return results


# from pprint import pprint
# pprint(influencers(temp))
# topics = ['style']
#
# for topic in topics:
#     print prepare_rank( topic)
