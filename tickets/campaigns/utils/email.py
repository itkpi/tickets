import logging

from campaigns.utils.pdf import generate_pdf
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from tickets.settings import REPLY_EMAIL, FROM_EMAIL


logger = logging.getLogger(__name__)


def notify_owner(ticket):
    logger.info("Sending the notification to {}".format(ticket.get_cart().email))
    headers = {'Reply-To': REPLY_EMAIL}
    email_body = render_to_string('campaigns/issuedticket_email.html', {'issuedticket': ticket,
                                                                        'site': Site.objects.get_current()})
    details_body = render_to_string('campaigns/issuedticket_pdf.html', {'issuedticket': ticket,
                                                                        'site': Site.objects.get_current()})
    pdf = generate_pdf(details_body)

    msg = EmailMessage("Ваш квиток на {}".format(ticket.get_cart().ticket_type.campaign.title), email_body,
                       FROM_EMAIL, [ticket.get_cart().email], headers=headers)
    msg.content_subtype = "html"
    if pdf:
        msg.attach('tedx-ticket.pdf', pdf, 'application/pdf')
    msg.send()
