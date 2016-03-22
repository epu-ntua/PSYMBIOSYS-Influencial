from tweetfluence.models import *

for corr in Week.objects.all():
    corr.save()