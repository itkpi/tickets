# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-26 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0012_auto_20160526_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
