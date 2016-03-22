from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls import url, include
from rest_framework import routers
from tweetfluence.api import *



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'influencers', InfluencerViewSet)
router.register(r'weeks', WeekViewSet)
router.register(r'correlations', CorrelationScoreViewSet)




urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('tweetfluence.urls')),
    url(r'^spark/', include('spark.urls')),
    url(r'^$', RedirectView.as_view(url='login', permanent=True)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
