import logging
from uuid import uuid4

from campaigns.models import IssuedTicket
from campaigns.utils.email import notify_owner

logger = logging.getLogger(__name__)


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