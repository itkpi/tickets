from campaigns.models import Cart
from campaigns.views.campaign_views import logger
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from liqpay.liqpay import LiqPay
from tickets.settings import LIQPAY_PUBLIC, LIQPAY_PRIVATE


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
            "server_url": self.request.build_absolute_uri(reverse('api-liqpay')),
            "result_url": self.request.build_absolute_uri(cart.get_absolute_url())
        }
        logger.info(liqpay_data)

        html = liqpay.cnb_form(liqpay_data)

        context['liqpay_form'] = html

        return context
