from uuid import uuid4

from campaigns.models import IssuedTicket
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from tickets.settings import REPLY_EMAIL, FROM_EMAIL


def notify_owner(ticket):
    headers = {'Reply-To': REPLY_EMAIL}
    body = render_to_string('campaigns/issuedticket_email.html', {'issuedticket': ticket})
    msg = EmailMessage("Ваш білет на {}".format(ticket.get_cart().ticket_type.campaign.title), body,
                       FROM_EMAIL, [ticket.get_cart().email], headers=headers)
    msg.content_subtype = "html"
    msg.send()


def issue_ticket(cart):
    ticket = IssuedTicket(uid=generate_ticket_uid(), ticket_type=cart.ticket_type)
    ticket.save()

    notify_owner(ticket)
    return ticket


def generate_ticket_uid():
    return "T-{}".format(uuid4())
