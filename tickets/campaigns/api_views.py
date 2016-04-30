import logging

from campaigns.models import Cart
from liqpay.liqpay import LiqPay
from restless.views import Endpoint
from tickets.settings import LIQPAY_PUBLIC, LIQPAY_PRIVATE

logger = logging.getLogger(__name__)


class HelloWorld(Endpoint):
    def get(self, request):
        name = request.params.get('name', 'World')
        return {'message': 'Hello, %s!' % name}

    def post(self, request):
        name = request.params.get('name', 'World')
        return {'message': 'POST Hello, %s!' % name}


class LiqPayS2S(Endpoint):
    def post(self, request, cart_uid):
        logger.info("API Call")
        cart = Cart.objects.get(uid=cart_uid)
        logger.info("cart {}".format(cart.uid))
        logger.info("POST {}".format(str(request.POST)))
        data = request.POST['data']
        signature = request.POST['signature']
        logger.info("data: {}, signature: {}".format(data, signature))

        liqpay = LiqPay(LIQPAY_PUBLIC, LIQPAY_PRIVATE)
        sign = liqpay.str_to_sign(LIQPAY_PRIVATE.encode() + data.encode() + LIQPAY_PRIVATE.encode())
        logger.info("calculated signature {}".format(sign))

        return {'status': 'OK'}
