from uuid import uuid4

from campaigns.models import Campaign, IssuedTicket, Cart, TicketCounter
from campaigns.models import TicketType
from campaigns.utils.ticket_utils import issue_ticket
from campaigns.views.tickets_views import available_tickettypes_queryset
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory


class TestAvailableTicketTypes(TestCase):
    fixtures = ['two_tickettypes.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.campaign = Campaign.objects.get(id=1)
        self.ticket_type_1 = TicketType.objects.get(id=1)
        self.ticket_type_2 = TicketType.objects.get(id=2)

    def test_no_counters(self):
        # should be unlimited tickets
        self.assert_available_tickets_count(2)

        for ticket_type in [self.ticket_type_1, self.ticket_type_2]:
            for _ in range(10):
                cart = Cart.objects.create(uid=uuid4(), ticket_type=ticket_type)
                issue_ticket(cart)

        self.assert_available_tickets_count(2)

    def test_separate_unlimited_counters(self):
        c1 = TicketCounter.objects.create(campaign=self.campaign, unlimited=True, amount=0)
        c2 = TicketCounter.objects.create(campaign=self.campaign, unlimited=True, amount=0)
        self.ticket_type_1.counter = c1
        self.ticket_type_1.save()
        self.ticket_type_2.counter = c2
        self.ticket_type_2.save()

        self.assert_available_tickets_count(2)

        for ticket_type in [self.ticket_type_1, self.ticket_type_2]:
            for _ in range(10):
                self.issue_ticket(ticket_type)

        self.assert_available_tickets_count(2)

    def test_separate_limited_counters(self):
        c1 = TicketCounter.objects.create(campaign=self.campaign, unlimited=False, amount=2)
        c2 = TicketCounter.objects.create(campaign=self.campaign, unlimited=False, amount=2)
        self.ticket_type_1.counter = c1
        self.ticket_type_1.save()
        self.ticket_type_2.counter = c2
        self.ticket_type_2.save()

        request = self.factory.get('/campaigns/')
        request.user = AnonymousUser()
        self.assert_available_tickets_count(2)

        self.issue_ticket(self.ticket_type_1)
        self.issue_ticket(self.ticket_type_1)
        self.assert_available_tickets_count(1)

        self.issue_ticket(self.ticket_type_2)
        self.issue_ticket(self.ticket_type_2)
        self.assert_available_tickets_count(0)

    def test_common_limited_counters(self):
        c = TicketCounter.objects.create(campaign=self.campaign, unlimited=False, amount=2)
        self.ticket_type_1.counter = c
        self.ticket_type_1.save()
        self.ticket_type_2.counter = c
        self.ticket_type_2.save()

        self.assert_available_tickets_count(2)

        self.issue_ticket(self.ticket_type_1)
        self.issue_ticket(self.ticket_type_2)
        self.assert_available_tickets_count(0)

    def assert_available_tickets_count(self, count):
        request = self.factory.get('/campaigns/')
        request.user = AnonymousUser()
        available = list(available_tickettypes_queryset(request, self.campaign))
        self.assertEqual(len(available), count)

    def issue_ticket(self, ticket_type):
        cart = Cart.objects.create(uid=uuid4(), ticket_type=ticket_type)
        issue_ticket(cart)
