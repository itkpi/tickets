import logging
from uuid import uuid4

from campaigns.models import IssuedTicket
from campaigns.utils.email_utils import notify_owner

logger = logging.getLogger(__name__)


def issue_ticket(cart):
    if cart.ticket is not None:
        logger.error("Cart already has ticket, issuing canceled")
        return cart.ticket
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


def do_checkin(ticket):
    logger.info("Guest with ticked {} checked in on the event".format(ticket.uid))
    ticket.checked_in = True
    ticket.save()
