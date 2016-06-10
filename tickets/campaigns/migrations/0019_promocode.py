# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-10 16:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0018_auto_20160531_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=200, unique=True)),
                ('ticket_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.TicketType')),
            ],
        ),
    ]