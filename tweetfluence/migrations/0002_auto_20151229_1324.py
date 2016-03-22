# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetfluence', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrelationScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('average_score', models.FloatField(default=0, null=True, blank=True)),
                ('updated', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('start_date', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='influencer',
            name='topics',
        ),
        migrations.AddField(
            model_name='correlationscore',
            name='influencer',
            field=models.ForeignKey(to='tweetfluence.Influencer'),
        ),
        migrations.AddField(
            model_name='correlationscore',
            name='topic',
            field=models.ForeignKey(to='tweetfluence.Topic'),
        ),
        migrations.AddField(
            model_name='correlationscore',
            name='weeks',
            field=models.ManyToManyField(to='tweetfluence.Week'),
        ),
    ]
