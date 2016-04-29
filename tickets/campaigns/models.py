from django.db import models


class Campaign(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=50)
    opened = models.BooleanField(default=False)

    def __str__(self):
        return '{} [{}]'.format(self.title, 'opened' if self.opened else 'closed')

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('campaign-details', args=[str(self.slug)])


class TicketType(models.Model):
    type = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.IntegerField()
    campaign = models.ForeignKey(Campaign)

    def __str__(self):
        return '"{}" ticket of campaign <{}>'.format(self.type, self.campaign)


class Cart(models.Model):
    uid = models.CharField(max_length=200, unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    ticket_type = models.ForeignKey(TicketType)

    def __str__(self):
        return self.uid


class IssuedTicket(models.Model):
    uid = models.CharField(max_length=200, unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    ticket_type = models.ForeignKey(TicketType)

    def __str__(self):
        return self.uid
