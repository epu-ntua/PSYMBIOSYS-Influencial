from tweetfluence.models import *
from random import uniform

# for cor in CorrelationScore.objects.all():
#     if cor.average_score==0:
#         cor.average_score = uniform(0,1)
#         influencer = Influencer.objects.get(id=cor.influencer.id)
#         influencer.topics.add(cor.topic)
#         cor.save()
#         influencer.save()
#         print influencer.id

for week in Week.objects.all():
    if week.score==0:
        week.score = uniform(0,1)
        week.save()


# for week in Week.objects.all():
#     week.save()