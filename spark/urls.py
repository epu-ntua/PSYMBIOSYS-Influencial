from django.conf.urls import *
import views

urlpatterns = [

    url(r'^$', views.api, name='Home Page'),
    url(r'^influencers/$', views.influencers),
    url(r'^influencers/social/$', views.influencers_social_network),
    url(r'^influencers/(?P<pk>\d+)/$', views.per_influencer_details),
    url(r'^graphs/$', views.topic_graph),
    url(r'^recommendations/$', views.recommendations),
]
