# -*- coding: utf-8 -*-

__author__ = 'Michael'


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

def prepare_rank(people, lista):

    f = open('pageRank_fashion_vone.txt','w')
    for person in people:
        for doc in lista:
            if person in doc['doc']['text'].replace('twitter:',''):
                if person == doc['doc']['user_screen_name'].replace('twitter:',''):
                    continue
                else:
                    print doc['doc']['user_screen_name'].replace('twitter:','')+" -neighbor- "+person
                    f.write(doc['doc']['user_screen_name'].replace('twitter:','')+" -neighbor- "+person+"\n")

    f.close()

import json
from pprint import pprint
from data_samples.ndresponse_level import temp
# from social_big_sample import temp
# from ultra_big_sample import temp
pprint(influencers(temp))

prepare_rank(influencers(temp),temp)