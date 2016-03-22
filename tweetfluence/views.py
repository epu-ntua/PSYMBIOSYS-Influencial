from django.shortcuts import render, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from tweetfluence.forms import LoginForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from tweetfluence.models import *
from tweetfluence.urls import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from tweetfluence_functions import http_url
import json
import requests
import random

def login(request):

    if request.method != 'POST':

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('Influencers Page'))

        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    else:

        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = login_form.fetch_user()
            auth_login(request, user)
            return HttpResponseRedirect(reverse('Influencers Page'))

        return render(request, 'login.html', {
            'login_form': login_form,
            'error': True
        })

@login_required
def influencers(request):

    influencers_endpoint = http_url(request.get_host(), 'spark/influencers')
    topics_endpoint = http_url(request.get_host(), 'api/topics')

    page = request.GET['page'] if request.is_ajax() else 1

    top_influencers = requests.get(url=influencers_endpoint, params={'page': page}).json()

    if request.is_ajax():
        return HttpResponse(render_to_string('influencers-section.html', {
            'top_influencers': top_influencers
        }))

    topics_objects = requests.get(url=topics_endpoint).json()
    topics_list = [str(topic['name']) for topic in topics_objects]
    sorted_topics_list = sorted(topics_list, key=str.lower)

    return render(request, 'influencers-new.html', {
        'user': request.user,
        'top_influencers': top_influencers,
        'topics': sorted_topics_list
    })


@login_required
def discussions(request):

    influencers_endpoint = http_url(request.get_host(), 'spark/influencers')
    topics_endpoint = http_url(request.get_host(), 'api/topics')
    topic_recommendations_endpoint = http_url(request.get_host(), 'spark/recommendations')

    topic_recommendations = requests.get(url=topic_recommendations_endpoint).json()


    return render(request, 'discussions.html', {
        'user': request.user,
        'recommendations': topic_recommendations
    })


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('Login Page'))


def arctic(request):

    json_file = open('arctic.json')
    return HttpResponse(
        json.dumps(
            json.load(json_file)
        )
    )