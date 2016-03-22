import logging
import json
import itertools

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import Settings
from django.shortcuts import render, redirect, get_object_or_404
from tweetfluence.models import Influencer, Topic, CorrelationScore

import requests
from django.core.paginator import Paginator
import random
from anlzer import top_topics
from create_graphs import prepare_rank
dummy_topics = top_topics(20)

@csrf_exempt
def api(request):
    logging.info("The server.views.api function operated normally.")

    response = {
        "@context": "http://schema.org/",
        "@type": "Person",
        "name": "Michael Petychakis",
        "jobTitle": "API Lama",
        "telephone": "(425) 123-4567",
        "url": "http://www.apilama.com"
    }

    return HttpResponse(json.dumps(response), status=200)

@csrf_exempt
def influencers(request):
    logging.info("The spark.views.influencers function operated normally.")

    p = int(request.GET.get("page",  "1"))

    response = []

    # for cor in CorrelationScore.objects.all():
    # if cor.average_score>=0:
    #     influencer = Influencer.objects.get(id=cor.influencer.id)

    results = Influencer.objects.filter(correlationscore__average_score__gte=0).distinct().order_by('-stars')

    # results = Influencer.objects.all().order_by('-stars')

    pages = Paginator(results, 12)

    for influencer in pages.page(p).object_list:

        inf_top_topics = []
        for topic in influencer.topics.all():
            inf_top_topics.append(topic.name)

        inf_top_topics = random.sample(inf_top_topics, 5)

        inf_top_topics = random.sample(dummy_topics,5)

        # TODO remove the lines below

        # if counter_topics <3:
        #
        #     randIndex = random.sample(range(len(dummy_topics)), 3-len(top_topics))
        #     randIndex.sort()
        #     rand = [dummy_topics[i] for i in randIndex]
        #     top_topics = top_topics +rand

        try:
            temp_response = {}
            temp_response["name"] = str(influencer.first_name )
            temp_response["twitter_name"] = influencer.twitter_username
            temp_response["twitter_image"] = influencer.image_link
            temp_response["id"] = influencer.id
            temp_response["pagerank_score"] = influencer.rank
            temp_response["top_topics"] = inf_top_topics
            temp_response["normalized_score"] = influencer.stars
            temp_response['social_network']= influencer.social_network
        except:
            continue

        response.append(temp_response)


    return HttpResponse(json.dumps(response), status=200)

@csrf_exempt
def influencers_social_network(request):
    logging.info("The spark.views.influencers function operated normally.")

    p = int(request.GET.get("page",  "1"))
    network = request.GET.get("network",  "twitter")

    response = []

    # for cor in CorrelationScore.objects.all():
    # if cor.average_score>=0:
    #     influencer = Influencer.objects.get(id=cor.influencer.id)

    results = Influencer.objects.filter(correlationscore__average_score__gte=0, social_network=network).distinct().order_by('-stars')

    # results = Influencer.objects.all().order_by('-stars')

    pages = Paginator(results, 12)

    for influencer in pages.page(p).object_list:

        inf_top_topics = []
        for topic in influencer.topics.all():
            inf_top_topics.append(topic.name)

        inf_top_topics = random.sample(inf_top_topics, 5)

        inf_top_topics = random.sample(dummy_topics,5)

        # TODO remove the lines below

        # if counter_topics <3:
        #
        #     randIndex = random.sample(range(len(dummy_topics)), 3-len(top_topics))
        #     randIndex.sort()
        #     rand = [dummy_topics[i] for i in randIndex]
        #     top_topics = top_topics +rand

        try:
            temp_response = {}
            temp_response["name"] = str(influencer.first_name )
            temp_response["twitter_name"] = influencer.twitter_username
            temp_response["twitter_image"] = influencer.image_link
            temp_response["id"] = influencer.id
            temp_response["pagerank_score"] = influencer.rank
            temp_response["top_topics"] = inf_top_topics
            temp_response["normalized_score"] = influencer.stars
            temp_response['social_network']= influencer.social_network
        except:
            continue

        response.append(temp_response)


    return HttpResponse(json.dumps(response), status=200)

@csrf_exempt
def per_influencer_details(request, pk):
    influencer = get_object_or_404(Influencer, pk=pk)
    logging.info("The spark.views.per_influencer_details function operated normally.")

    top_topics = []
    for topic in influencer.topics.all():
        top_topics.append(topic.name)
    # TODO remove the lines below

    randIndex = random.sample(range(len(dummy_topics)), 3)
    randIndex.sort()
    rand = [dummy_topics[i] for i in randIndex]

    top_topics = top_topics +rand
    
    temp_response = {}
    temp_response["name"] = str(influencer.first_name )
    temp_response["twitter_name"] = influencer.twitter_username
    temp_response["twitter_image"] = influencer.image_link
    temp_response["pagerank_score"] = influencer.rank
    temp_response["top_topics"] = top_topics
    temp_response["normalized_score"] = influencer.stars
    temp_response['social_network']= influencer.social_network

    topics_averages = []
    topics_values = []
    counter = 0
    for topic in Topic.objects.all():
        if CorrelationScore.objects.filter(topic=topic,influencer=influencer):
            corr = CorrelationScore.objects.filter(topic=topic,influencer=influencer)[0]
            if corr.average_score<=0:
                continue
            counter = counter + 1
            if counter>5:
                break
            if not corr.average_score:
                continue

            topics_averages.append({
                "name": topic.name,
                "average_score":corr.average_score

            })

            for week in corr.weeks.all():
                topics_values.append({
                    "name": topic.name,
                    "start":str(week.start_date),
                    "score":week.score
                })


    temp_response["topics_values"] = topics_values
    temp_response["topics_averages"] = topics_averages

    return HttpResponse(json.dumps(temp_response), status=200)

@csrf_exempt
def topic_graph(request):

    if request.method != 'GET':
        return HttpResponseBadRequest('Only accepting HTTP GET requests!')

    topics = request.GET.getlist('topics[]')
    print topics
    temp_response = {'data': []}
    for topic in topics:
        temp_response['data'] += prepare_rank(str(topic))

    temp = [d.items() for d in temp_response['data']]
    temp.sort()
    response = list(dict(temp) for temp, _ in itertools.groupby(temp))
    print '1'
    print response
    print '2'
    return HttpResponse(json.dumps(response), status=200)


@csrf_exempt
def recommendations(request):

    results = {}
    dummy_topics = top_topics(30)
    for topic in dummy_topics:
        randIndex = random.sample(range(len(dummy_topics)), 3)
        randIndex.sort()
        rand = [dummy_topics[i] for i in randIndex]
        results[topic] = rand


    return HttpResponse(json.dumps(results), status=200)
