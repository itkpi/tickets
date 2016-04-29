import logging
from uuid import uuid4

from campaigns.models import Campaign, TicketType, Cart, IssuedTicket
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View

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


class TicketDetailView(DetailView):
    model = IssuedTicket

    def get_slug_field(self):
        return 'uid'
