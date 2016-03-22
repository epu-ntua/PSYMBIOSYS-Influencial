# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetfluence', '0002_auto_20151229_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='topics',
            field=models.ManyToManyField(to='tweetfluence.Topic'),
        ),
        migrations.AlterField(
            model_name='correlationscore',
            name='weeks',
            field=models.ManyToManyField(related_name='week_scores', to='tweetfluence.Week'),
        ),
    ]
