# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-23 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0024_auto_20160921_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='telefono',
            field=models.CharField(default=3517035878, max_length=128),
            preserve_default=False,
        ),
    ]
