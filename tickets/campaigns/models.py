from django.db import models


class Campaign(models.Model):
    title = models.CharField(max_length=200)
    opened = models.BooleanField(default=False)


class TicketType(models.Model):
    type = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.IntegerField()
    campaign = models.ForeignKey(Campaign)
