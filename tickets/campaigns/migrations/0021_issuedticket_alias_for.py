# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-24 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0020_promocode_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuedticket',
            name='alias_for',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
