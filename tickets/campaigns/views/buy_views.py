from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import DetailView
from liqpay.liqpay import LiqPay

from campaigns.models import Cart, LiqPayData
from campaigns.utils.ticket_utils import issue_ticket
from campaigns.views.campaign_views import logger
from campaigns.views.tickets_views import present_tickettypes_queryset
from tickets.settings import LIQPAY_PUBLIC, LIQPAY_PRIVATE


class CartDetailView(DetailView):
    model = Cart

    def get_slug_field(self):
        return 'uid'

    def get(self, request, **kwargs):
        cart = self.get_object()
        if cart.status == Cart.CART_CREATED:
            if cart.ticket_type.cost == 0:
                issue_ticket(cart)
            is_present = present_tickettypes_queryset(request, cart.ticket_type.campaign).filter(id=cart.ticket_type.id)\
                .exists()
            if not is_present:
                raise Http404()

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        cart = self.get_object()
        context = super().get_context_data(**kwargs)

        if cart.status != Cart.TICKET_ISSUED:
            html = self.get_liqpay_form(cart)
            context['liqpay_form'] = html

        context['liqpay_data'] = LiqPayData.objects.filter(cart=cart).order_by('-timestamp').first()

        return context

    def get_liqpay_form(self, cart):
        liqpay = LiqPay(LIQPAY_PUBLIC, LIQPAY_PRIVATE)
        liqpay_data = {
            "action": "pay",
            "amount": str(cart.ticket_type.cost),
            "currency": "UAH",
            "description": "{} ticket for {}".format(cart.ticket_type.type, cart.ticket_type.campaign.title),
            "order_id": cart.uid,
            "language": "ru",
            "sandbox": cart.ticket_type.campaign.sandbox,
            "server_url": self.request.build_absolute_uri(reverse('api-liqpay')),
            "result_url": self.request.build_absolute_uri(cart.get_absolute_url())
        }
        logger.info(liqpay_data)
        html = liqpay.cnb_form(liqpay_data)
        return html
