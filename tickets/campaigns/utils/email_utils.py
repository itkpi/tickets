import logging

from campaigns.utils.pdf_utils import generate_pdf
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from tickets.settings import REPLY_EMAIL, FROM_EMAIL, GOOGLE_MAPS_KEY

logger = logging.getLogger(__name__)


def notify_owner(ticket):
    if ticket.get_cart().email is None:
        logger.info("Email is not set. Notification for ticket {} canceled.".format(ticket.uid))
        return
    logger.info("Sending the notification to {}".format(ticket.get_cart().email))
    headers = {'Reply-To': REPLY_EMAIL}
    email_body = render_to_string('campaigns/issuedticket_detail.html', {'issuedticket': ticket,
                                                                         'site': Site.objects.get_current(),
                                                                         'email': True,
                                                                         'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY})
    details_body = render_to_string('campaigns/issuedticket_pdf.html', {'issuedticket': ticket,
                                                                           'site': Site.objects.get_current(),
                                                                           'pdf': True,
                                                                           'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY})
    pdf = generate_pdf(details_body)

    msg = EmailMessage("Ваш квиток на {}".format(ticket.get_cart().ticket_type.campaign.title), email_body,
                       FROM_EMAIL, [ticket.get_cart().email], headers=headers)
    msg.content_subtype = "html"
    if pdf:
        msg.attach('tedx-ticket.pdf', pdf, 'application/pdf')
    msg.send()
