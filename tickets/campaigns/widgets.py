import re

from dashing.widgets import NumberWidget, ListWidget, KnobWidget
from django.db.models import Count, Sum

from campaigns.models import IssuedTicket, Campaign, TicketCounter, TicketType


def get_tickets_queryset():
    return IssuedTicket.objects. \
        exclude(cart__ticket_type__type='Test Ticket')


class TicketsSoldWidget(NumberWidget):
    title = 'Продані квитки'

    def get_value(self):
        return get_tickets_queryset().count()

    def get_detail(self):
        counts = get_tickets_queryset().values('cart__ticket_type__campaign').\
            annotate(c_count=Count('cart__ticket_type__campaign'))
        print(counts)
        return '\n'.join('{cart__ticket_type__campaign}: {c_count}'.format(**campaign) for campaign in counts)

    def get_more_info(self):
        return ''


class TicketsTypesWidget(ListWidget):
    title = 'За типом квитка'

    def get_data(self):
        counts = get_tickets_queryset().values('cart__ticket_type', 'cart__ticket_type__type'). \
            annotate(c_count=Count('cart__ticket_type'))
        return [{'label': self.remove_brackets(campaign['cart__ticket_type__type']), 'value': campaign['c_count']} for campaign in counts]

    def remove_brackets(self, name):
        return re.sub(r"\([^)]*\)", '', name)


class CoutersWidget(KnobWidget):
    title = 'Кількість проданих'

    def get_value(self):
        return get_tickets_queryset().count()

    def get_data(self):
        amount = self.get_amount()

        return {
            'min': 0,
            'max': amount,
            'readOnly': True,
        }

    def get_amount(self):
        return TicketType.objects.exclude(public=False).values('counter__amount', 'counter__id').distinct(). \
            aggregate(Sum('counter__amount'))['counter__amount__sum']

    def get_detail(self):
        return "{} квитків у продажу".format(self.get_amount())
