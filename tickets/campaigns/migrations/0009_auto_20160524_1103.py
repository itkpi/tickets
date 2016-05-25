# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_auto_20160524_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Item in cart'), ('TICKET_ISSUED', 'Payment confirmed, ticket issued'), ('PAYMENT_FAILED', 'Payment failed'), ('PAYMENT_WAIT_ACCEPT', 'Payment is waiting for acceptance...'), ('UNKNOWN_STATUS', 'Unknown status, check LiqPay data')], default='CREATED', max_length=25),
        ),
    ]