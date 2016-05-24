import base64
import json
import logging
from uuid import uuid4

from campaigns.models import Cart, LiqPayData, IssuedTicket
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
        data, signature = request.POST['data'], request.POST['signature']

        calc_sign = self.calculate_signature(data)
        logger.info("LIQPAY: data: {}, signature: {}, calculated signature {}".format(
            data, signature, calc_sign))

        if signature != calc_sign:
            logger.error("LIQPAY: WRONG SIGNATURE, signature: {}, calculated signature {}".format(
                signature, calc_sign))
            return {'status': 'ERROR'}

        b64_decoded = base64.b64decode(data).decode()
        logger.info("LIQPAY: decoded = {}".format(b64_decoded))
        decoded = json.loads(b64_decoded)
        cart = Cart.objects.get(uid=decoded['order_id'])

        self.persist_api_call(cart, decoded)

        if decoded['status'] in ['failure', 'error']:
            self.payment_failed(cart)
        elif decoded['status'] in ['success', 'sandbox']:
            self.payment_successful(cart)
        elif decoded['status'] in ['wait_accept']:
            self.payment_wait_accept(cart)
        else:
            self.payment_unknown_status(cart)
        return {'status': 'OK'}

    def payment_wait_accept(self, cart):
        cart.status = cart.PAYMENT_WAIT_ACCEPT
        cart.save()

    def payment_unknown_status(self, cart):
        cart.status = cart.UNKNOWN_STATUS
        cart.save()

    def payment_failed(self, cart):
        cart.status = cart.PAYMENT_FAILED
        cart.save()

    def payment_successful(self, cart):
        ticket = IssuedTicket(uid="T-{}".format(uuid4()), ticket_type=cart.ticket_type)
        ticket.save()
        cart.ticket = ticket
        cart.status = cart.TICKET_ISSUED
        cart.save()

    def persist_api_call(self, cart, decoded):
        lp_data = LiqPayData(cart=cart)
        for key, value in decoded.items():
            lp_key = "lp_{}".format(key)
            if hasattr(lp_data, lp_key):
                logger.info("set {}.{}={}".format(cart.uid, lp_key, value))
                setattr(lp_data, lp_key, value)
        lp_data.save()

    def calculate_signature(self, data):
        liqpay = LiqPay(LIQPAY_PUBLIC, LIQPAY_PRIVATE)
        calc_sign = liqpay.str_to_sign(LIQPAY_PRIVATE.encode() + data.encode() + LIQPAY_PRIVATE.encode()).decode()
        return calc_sign
