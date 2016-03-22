from django.conf.urls import *
from tweetfluence import views


urlpatterns = [

    url(r'^login$', views.login, name='Login Page'),
    url(r'^logout', views.logout, name='Logout Page'),
    url(r'^influencers$', views.influencers, name='Influencers Page'),
    url(r'^discussions', views.discussions, name='Discussions Page'),

]
