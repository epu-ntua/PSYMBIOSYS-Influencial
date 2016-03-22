from tweetfluence.models import *
from spark.twitter_api import *
from time import sleep

for i in Influencer.objects.filter(first_name = "empty"):
        member = profile(i.twitter_username)
        i.first_name = member['full_name']
        i.image_link = member['profile_image_url']
        i.save()
        sleep(10)
        print i.id
