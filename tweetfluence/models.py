from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_init, pre_delete, post_delete



class Topic(models.Model):
    name = models.CharField(max_length=75)
    twitter_hashtag = models.CharField(max_length=100, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name


class Influencer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    twitter_username = models.CharField(max_length=100)
    image_link = models.URLField()
    rank = models.FloatField(default=0)
    stars = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(blank=False, null=False)
    topics = models.ManyToManyField(Topic)
    social_network = models.CharField(max_length=100, default="")

    def __unicode__(self):
        return self.twitter_username

class Week(models.Model):
    score = models.FloatField()
    start_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return str(self.id)


class CorrelationScore(models.Model):
    influencer = models.ForeignKey(Influencer)
    topic = models.ForeignKey(Topic)
    weeks = models.ManyToManyField(Week, related_name="week_scores")
    average_score = models.FloatField(null=True, blank=True, default=0)
    updated = models.DateTimeField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return str(self.topic.name)+"--"+str(self.influencer.twitter_username)+"--"+str(self.average_score)+"--"+str(self.influencer.id)


def calculate_average_score(sender, **kwargs):
        week = kwargs.get('instance')
        if not week.week_scores.all():
            return 1

        else:
            correlation = CorrelationScore.objects.get(id=week.week_scores.all()[0].id)
            score = 0
            if correlation.weeks:
                weeks = correlation.weeks.all()
                for week in weeks:
                    score = score + week.score

                correlation.average_score = score / (len(weeks)*1.0)

            correlation.save()


post_save.connect(calculate_average_score, sender=Week)
