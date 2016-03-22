# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetfluence', '0003_auto_20160114_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='social_network',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
