from campaigns.models import IssuedTicket, TicketType, Campaign, Cart
from campaigns.utils.ticket_utils import do_checkin, issue_ticket
from django.core import mail
from django.test import TestCase


class TestTicketUtils(TestCase):
    fixtures = ['simple.json']

    def setUp(self):
        self.campaign = Campaign.objects.get(id=1)
        self.ticket_type = TicketType.objects.filter(campaign=self.campaign).first()

    def test_do_checkin(self):
        ticket = IssuedTicket.objects.create(uid="T-TEST", ticket_type=self.ticket_type)
        self.assertFalse(ticket.checked_in)

        do_checkin(ticket)

        ticket.refresh_from_db()
        self.assertTrue(ticket.checked_in)

    def test_issue_ticket(self):
        cart = Cart.objects.create(ticket_type=self.ticket_type)
        self.assertEqual(cart.status, Cart.CART_CREATED)
        self.assertEqual(cart.ticket, None)

        issue_ticket(cart)
        self.assertEqual(cart.status, Cart.TICKET_ISSUED)
        self.assertNotEqual(cart.ticket, None)

        self.assertEqual(len(mail.outbox), 0)

    def test_issue_ticket_notification(self):
        cart = Cart.objects.create(ticket_type=self.ticket_type, email="test@example.com")
        issue_ticket(cart)
        self.assertEqual(len(mail.outbox), 1)
