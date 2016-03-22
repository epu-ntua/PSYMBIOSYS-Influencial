from datetime import datetime

import requests
from pyspark import SparkContext
from pyspark.mllib.stat import Statistics
from anlzer import *
from algorithms.pagerank import *
from twitter_api import profile
from datetime import datetime, date, timedelta
import calendar

"""
Command to run this:
C:\Syncfusion\BigDataSDK\2.1.0.77\SDK\Spark\bin\pyspark worker.py
"""


def create_or_update_influencer(influencer):
    url = "http://localhost:8000/api/influencers/"
    try:
        member = profile(influencer['username'])
    except:
        member = {
            'full_name': 'empty',
            'profile_image_url': "https://twitter.com/"+influencer['username']
        }

    first_name = member['full_name'].encode('ascii','ignore')
    print first_name
    last_name = "blank"
    username = influencer['username']
    rank = influencer['score']
    stars = 2.2
    if not first_name:
        first_name = " "
    print type(first_name)

    # TODO store this metric somewhere
    # metric = member['metric']

    updated = str(datetime.now())
    image_link = member['profile_image_url']
    payload = '{    "first_name": "%s",    "last_name": "%s",    "twitter_username": "%s",    "image_link": "%s",    "rank": %f,    "stars": %f,    "updated": "%s",    "topics": [4]}' % (
        first_name, last_name, username, image_link, rank, stars, updated)

    headers = {
        'authorization': "Basic ZGV2OjEyMzQ=",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "e283380d-e1e7-4aad-a27c-cdd34f5dc096"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print response.json()

    return {"username":username,"id":response.json()['id']}

def create_or_update_topic(topic):

    url = "http://localhost:8000/api/topics/"
    
    payload = '{"name": "%s",    "twitter_hashtag": "#%s"}'%(topic,topic)
    headers = {
        'authorization': "Basic ZGV2OjEyMzQ=",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "589d44c5-8307-49ed-b5e2-07729106f6a0"
        }


    response = requests.request("POST", url, data=payload, headers=headers)

    return {"topic":topic,"id":response.json()['id']}

def anlzer_api_consumers(week=None):
    pass


def anlzer_api_topics(week=None):
    pass


def calculate_page_rank():
    sc = SparkContext(appName="PythonPageRank")

    lines = sc.textFile("pageRank_fashion_vone.txt")
    print "##########################################"
    print "file loaded on hdfs"
    print "##########################################"

    # Loads all URLs from input file and initialize their neighbors.
    links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()

    # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(3):
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(
                lambda url_urls_rank: computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

    influencers = []

    for (link, rank) in ranks.collect():
        print("%s has rank: %s." % (link, rank))
        influencers.append({"username": str(link), "score": rank})

    sc.stop()

    return influencers


def identify_graphs(influencers):
    pass


def create_or_update_week(influencer_tweets, topic_tweets, week):

    topic_cor = []
    influencer_cor = []
    for t in topic_tweets:
        for i in influencer_tweets:
            if t['time'] == i['time']:
                topic_cor.append(t['count'])
                influencer_cor.append(i['count'])

    if len(topic_cor)<=1:
        corr = 0
    else:

        sc = SparkContext(appName="CorrelationPerWeek")

        topic_tweets = sc.parallelize(topic_cor)
        influencer_tweets = sc.parallelize(influencer_cor)

        corr = Statistics.corr(topic_tweets, influencer_tweets, "pearson")

        sc.stop()

    url = "http://localhost:8000/api/weeks/"

    today = datetime.fromtimestamp(week/1000.0)
    payload = '{    "score": %f,    "start_date": "%s"  }' % (
        float(corr), str(today.year) + "-" + str(today.month) + "-" + str(today.day))
    headers = {
        'authorization': "Basic ZGV2OjEyMzQ=",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "7c8668c0-a4c2-f42d-66a9-95cbfb7806c5"
    }

    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        return  response.json()['id']
    except:
        print "error"

    return 1


def create_or_update_correlation(influencer, topic, weeks):
    url = "http://localhost:8000/api/correlations/"

    """
    Sample Payload
    '{    "average_score": null,    "influencer": 1,    "topic": 1,    "updated": "2015-12-29T13:35:17Z",    "weeks": [1,2,3]}'
    """

    payload = '{    "average_score": null,    "influencer": %d,    "topic": %d,    "updated": "%s",    "weeks": [' % (
        int(influencer), int(topic), str(datetime.now()))
    if weeks:
        if len(weeks) == 1:
            payload = payload + str(weeks[0])
        else:
            payload = payload + str(weeks[0]) + ","
            counter = 1
            while counter < len(weeks) - 1:
                payload = payload + str(weeks[counter]) + ","
                counter = counter + 1
            payload = payload + str(weeks[len(weeks) - 1])
    payload = payload + ']}'

    headers = {
        'authorization': "Basic ZGV2OjEyMzQ=",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "778df331-05f1-b676-ac56-c3266dbd0ae6"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

influencers = []

influencers_ranks = calculate_page_rank()
counter = 0

topics = []
# topics_raw = ['gold','dior','sofa', 'red','gucci','armani','burberry']
topics_raw = top_topics(10)

for topic in topics_raw:
    topics.append(create_or_update_topic(topic))

for influencer in influencers_ranks:
    counter = counter + 1
    if counter >=80:
        break
    try:
        influencers.append(create_or_update_influencer(influencer))
    except:
        continue



# TODO enable graph traversing
# graphs = identify_graphs(influencers)


weeks = [1, 2, 3, 4, 5, 6, 7, 8]
results = {}




# TODO make this weeks


for day in [date(2016, 1, 12),date(2016, 1, 19),date(2016, 1, 25),date(2016, 2, 2)]:

    from_timestamp = calendar.timegm(day.timetuple())
    from_timestamp = int(str(from_timestamp)+"000")

    date_1 =  datetime.fromtimestamp(from_timestamp/1000.0)

    end_date = date_1 + timedelta(days=7)

    until_timestamp = calendar.timegm(end_date.timetuple())

    until_timestamp = int(str(until_timestamp)+"000")


    anlzer_res = parse_anlzer_weeks(topics=topics_raw,accounts=influencers,from_timestamp=from_timestamp,until_timestamp=until_timestamp)

    for topic in topics:
        for influencer in influencers:
                topic_res = anlzer_res[topic['topic']]['entries']
                influencer_res = anlzer_res[str(topic['topic']) + "-" + 'twitter:'+str(influencer['username'])]['entries']
                if not str(topic['topic']) + "-" + str(influencer['username']) in results:
                    results[str(topic['topic']) + "-" + str(influencer['username'])] = []
                results[str(topic['topic']) + "-" + str(influencer['username'])].append(
                        create_or_update_week(influencer_tweets=influencer_res, topic_tweets=topic_res, week=from_timestamp))

    for topic in topics:
        for influencer in influencers:
            # TODO remove the lines below
            influencer_id = influencer['id']
            topic_id = topic['id']

            create_or_update_correlation(influencer=influencer_id, topic=topic_id,
                                         weeks=results[str(topic['topic']) + "-" +str(influencer['username'])])