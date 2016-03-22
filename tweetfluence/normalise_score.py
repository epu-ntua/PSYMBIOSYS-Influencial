from random import randint

from tweetfluence.models import *

for i in Influencer.objects.all():

        rank = ((i.rank/2.0)*3) % 5
        i.stars = round(rank*2)/2
        if i.stars <1:
            i.stars = randint(1,5)
        i.save()

total_score = 0
max_ = 0
min_ = 0


# for i in Influencer.objects.all():
#     total_score = total_score + i.rank
#     if i.rank > max_:
#         max_ = i.rank
#     if i.rank < min_:
#         min_ = i.rank
#
# average = total_score/len(Influencer.objects.all())*1.0