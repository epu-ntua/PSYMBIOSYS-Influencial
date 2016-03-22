from rest_framework import serializers, viewsets
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
import requests


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic

    def create(self, validated_data):
        if Topic.objects.filter(name=validated_data['name']):
            topic = Topic.objects.filter(name=validated_data['name'])[0]
            return topic
        else:
            topic = Topic.objects.create(  name = validated_data['name'], \
                                                 twitter_hashtag = validated_data['twitter_hashtag'])
            return topic

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class InfluencerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Influencer

    def create(self, validated_data):
        if Influencer.objects.filter(twitter_username=validated_data['twitter_username']):
            person = Influencer.objects.filter(twitter_username=validated_data['twitter_username'])[0]
            return person
        else:
            person = Influencer.objects.create(  first_name = validated_data['first_name'], \
                                                 last_name = validated_data['last_name'], \
                                                 twitter_username = validated_data['twitter_username'], \
                                                 image_link = validated_data['image_link'], \
                                                 rank = validated_data['rank'], \
                                                 stars = validated_data['stars'], \
                                                 updated=validated_data['updated'])
            return person

class InfluencerViewSet(viewsets.ModelViewSet):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer

class CorrelationScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrelationScore

    def create(self, validated_data):
        if CorrelationScore.objects.filter(influencer=validated_data['influencer'],topic=validated_data['topic']):
            corr = CorrelationScore.objects.filter(influencer=validated_data['influencer'],topic=validated_data['topic'])[0]

            for week in validated_data['weeks']:
                corr.weeks.add(week)
            corr.save()

            return corr
        else:
            corr = CorrelationScore.objects.create( influencer = validated_data['influencer'], \
                                                 topic = validated_data['topic'], \
                                                 average_score = validated_data['average_score'], \
                                                 updated = validated_data['updated'])

            return corr

class CorrelationScoreViewSet(viewsets.ModelViewSet):
    queryset = CorrelationScore.objects.all()
    serializer_class = CorrelationScoreSerializer


class WeekSerializer(serializers.ModelSerializer):
    # week_scores = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Week

class WeekViewSet(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer