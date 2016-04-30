import base64
import json
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
    def post(self, request):
        logger.info("LIQPAY: API Call from LiqPay: {}".format(str(request.POST)))
        data = request.POST['data']
        signature = request.POST['signature']

        liqpay = LiqPay(LIQPAY_PUBLIC, LIQPAY_PRIVATE)
        calc_sign = liqpay.str_to_sign(LIQPAY_PRIVATE.encode() + data.encode() + LIQPAY_PRIVATE.encode()).decode()
        logger.info("LIQPAY: data: {}, signature: {}, calculated signature {}".format(
            data, signature, calc_sign))

        if signature != calc_sign:
            logger.error("LIQPAY: WRONG SIGNATURE, signature: {}, calculated signature {}".format(
                signature, calc_sign))
            return {'status': 'ERROR'}

        decoded = json.loads(base64.b64decode(data).decode())
        cart = Cart.objects.get(uid=decoded['order_id'])
        for key,value in decoded.items():
            lp_key = "lp_{}".format(key)
            if hasattr(cart, lp_key):
                setattr(cart, lp_key, value)
        cart.save()

        return {'status': 'OK'}
