import logging
from uuid import uuid4

from campaigns.models import IssuedTicket
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from tickets.settings import REPLY_EMAIL, FROM_EMAIL


logger = logging.getLogger(__name__)


def notify_owner(ticket):
    logger.info("Sending the notification to {}".format(ticket.get_cart().email))
    headers = {'Reply-To': REPLY_EMAIL}
    body = render_to_string('campaigns/issuedticket_email.html', {'issuedticket': ticket,
                                                                  'site': Site.objects.get_current()})
    msg = EmailMessage("Ваш квиток на {}".format(ticket.get_cart().ticket_type.campaign.title), body,
                       FROM_EMAIL, [ticket.get_cart().email], headers=headers)
    msg.content_subtype = "html"
    msg.send()


def issue_ticket(cart):
    ticket = IssuedTicket(uid=generate_ticket_uid(), ticket_type=cart.ticket_type)
    ticket.save()
    cart.ticket = ticket
    cart.status = cart.TICKET_ISSUED
    cart.save()

    logger.info("Ticket {} issued".format(ticket.uid))

    notify_owner(ticket)
    return ticket


def generate_ticket_uid():
    return "T-{}".format(uuid4())
