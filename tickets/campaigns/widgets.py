import datetime
import re

from dashing.widgets import NumberWidget, ListWidget, KnobWidget, GraphWidget
from django.db.models import Count, Sum

from campaigns.models import IssuedTicket, TicketType


def remove_brackets(name):
    return re.sub(r"\([^)]*\)", '', name)


def get_tickets_queryset():
    return IssuedTicket.objects. \
        exclude(cart__ticket_type__type='Test Ticket')


class TicketsSoldWidget(NumberWidget):
    """
    Deprecated
    """

    title = 'Продані квитки'

    def get_value(self):
        return get_tickets_queryset().count()

    def get_detail(self):
        counts = get_tickets_queryset(). \
            exclude(cart__ticket_type__cost=0). \
            values('cart__ticket_type__campaign'). \
            annotate(c_count=Count('cart__ticket_type__campaign'))
        return '\n'.join('{cart__ticket_type__campaign}: {c_count}'.format(**campaign) for campaign in counts)
    def get_more_info(self):
        return ''




class TicketsTypesWidget(ListWidget):
    title = 'За типом квитка'

    def get_data(self):
        counts = get_tickets_queryset().values('cart__ticket_type', 'cart__ticket_type__type'). \
            annotate(c_count=Count('cart__ticket_type'))
        return [{'label': remove_brackets(campaign['cart__ticket_type__type']), 'value': campaign['c_count']} for campaign in counts]


class CoutersWidget(KnobWidget):
    title = 'Кількість проданих'

    def get_value(self):
        return get_tickets_queryset(). \
            exclude(cart__ticket_type__cost=0). \
            count()

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


class DaysWidget(GraphWidget):
    title = 'Сьогодні'

    def get_value(self):
        today = datetime.date.today()

        today_tickets = get_tickets_queryset(). \
            filter(timestamp__gt=today,
                   timestamp__lt=today + datetime.timedelta(1))

        # return "{} + ({} free)".format(today_tickets.exclude(cart__ticket_type__cost=0).count(), today_tickets.filter(cart__ticket_type__cost=0).count())
        return "{}".format(today_tickets.count())

    def get_data(self):
        data = []
        single_date = datetime.date(2016, 6, 1)
        end_date = datetime.date.today()
        day = 1
        while single_date < end_date:
            single_date += datetime.timedelta(1)
            amount = get_tickets_queryset().filter(timestamp__gt=single_date,
                                                   timestamp__lt=single_date + datetime.timedelta(1)).\
                count()
            data.append({'x': day, 'y': amount})
            day += 1

        return data

    def get_amount(self):
        return TicketType.objects.exclude(public=False).values('counter__amount', 'counter__id').distinct(). \
            aggregate(Sum('counter__amount'))['counter__amount__sum']

    def get_more_info(self):
        today = datetime.date.today()

        today_tickets = get_tickets_queryset(). \
            filter(timestamp__gt=today,
                   timestamp__lt=today + datetime.timedelta(1)). \
            filter(cart__ticket_type__cost=0)
        return "з них {} промо".format(today_tickets.count())


class Last10PeopleWidget(ListWidget):
    title = 'Останні 10 покупців'

    def get_data(self):
        tickets = get_tickets_queryset().order_by('-timestamp')[:10]
        return [{'label': '{} {}'.format(ticket.cart_set.first().name, ticket.cart_set.first().surname), 'value': ''} for ticket in tickets]


class TodayWidget(ListWidget):
    title = 'Сьогодні квитків видано'

    def get_data(self):
        today = datetime.date.today()

        today_tickets = get_tickets_queryset(). \
            filter(timestamp__gt=today,
                   timestamp__lt=today + datetime.timedelta(1))

        counts = today_tickets.values('cart__ticket_type', 'cart__ticket_type__type'). \
            annotate(c_count=Count('cart__ticket_type'))
        return [{'label': remove_brackets(campaign['cart__ticket_type__type']), 'value': campaign['c_count']} for
                campaign in counts]


class AllTicketsWidget(KnobWidget):
    title = 'Загальна кількість'
    detail = '(включаючи промо)'

    def get_value(self):
        return get_tickets_queryset(). \
            count()

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
