import logging
from uuid import uuid4

from campaigns.models import Campaign, TicketType, Cart, IssuedTicket
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from liqpay.liqpay import LiqPay
from tickets.settings import LIQPAY_PUBLIC, LIQPAY_PRIVATE

logger = logging.getLogger(__name__)


class CampaignListView(ListView):
    model = Campaign
    queryset = Campaign.objects.filter(opened=True)


class CampaignDetailView(DetailView):
    model = Campaign


class TicketTypeListView(ListView):
    model = TicketType

    def get_queryset(self):
        campaign = Campaign.objects.get(slug=self.kwargs['campaign_slug'])
        return TicketType.objects.filter(campaign=campaign)


class BuyTicketView(View):
    def post(self, request, *args, **kwargs):
        tickettype = TicketType.objects.get(id=int(self.kwargs['tickettype_id']))

        cart = Cart(uid="CART-{}".format(uuid4()),
                    ticket_type=tickettype)
        cart.save()
        logger.info('Ticket {} added to cart {}'.format(tickettype, cart))
        return redirect(cart.get_absolute_url())


class CartDetailView(DetailView):
    model = Cart

    def get_slug_field(self):
        return 'uid'

    def get_context_data(self, **kwargs):
        cart = self.get_object()
        context = super().get_context_data(**kwargs)

        liqpay = LiqPay(LIQPAY_PUBLIC, LIQPAY_PRIVATE)
        liqpay_data = {
            "action": "pay",
            "amount": str(cart.ticket_type.cost),
            "currency": "UAH",
            "description": "{} ticket for {}".format(cart.ticket_type.type, cart.ticket_type.campaign.title),
            "order_id": cart.uid,
            "language": "ru",
            "sandbox": cart.ticket_type.campaign.sandbox,
            "server_url": self.request.build_absolute_uri(reverse('api-liqpay', args=(cart.uid,))),
            "result_url": self.request.build_absolute_uri(cart.get_absolute_url())
        }
        logger.info(liqpay_data)

        html = liqpay.cnb_form(liqpay_data)

        context['liqpay_form'] = html

        return context


class TicketDetailView(DetailView):
    model = IssuedTicket

    def get_slug_field(self):
        return 'uid'
