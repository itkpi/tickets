from django.db import models


class Campaign(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=50)
    opened = models.BooleanField(default=False)
    sandbox = models.BooleanField(default=True)
    description = models.TextField(default="")
    place = models.CharField(max_length=400, default="<no place>")
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return '{} [{}]'.format(self.title, 'opened' if self.opened else 'closed')

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('campaign-details', args=[self.slug])


class TicketCounter(models.Model):
    amount = models.IntegerField()
    unlimited = models.BooleanField(default=False)
    campaign = models.ForeignKey(Campaign)

    def __str__(self):
        if self.unlimited:
            return '<{}: {}, [unlimited]>'.format(self.id, self.campaign, self.unlimited)
        else:
            return '<{}: {}, [{}]>'.format(self.id, self.campaign, self.amount)


class TicketType(models.Model):
    type = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    public = models.BooleanField(default=True)
    campaign = models.ForeignKey(Campaign)
    available_from = models.DateTimeField(null=True, blank=True)
    available_till = models.DateTimeField(null=True, blank=True)
    counter = models.ForeignKey(TicketCounter, null=True)

    def __str__(self):
        return '"{}" ticket of <{}>'.format(self.type, self.campaign)


class IssuedTicket(models.Model):
    uid = models.CharField(max_length=200, unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    ticket_type = models.ForeignKey(TicketType)
    checked_in = models.BooleanField(default=False)
    alias_for = models.CharField(max_length=200, null=False, blank=True, default='')

    def __str__(self):
        return self.uid

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('ticket-details', args=[self.uid])

    def get_cart(self):
        return self.cart_set.first()


class Cart(models.Model):
    CART_CREATED = 'CREATED'
    TICKET_ISSUED = 'TICKET_ISSUED'
    PAYMENT_FAILED = 'PAYMENT_FAILED'
    PAYMENT_WAIT_ACCEPT = 'PAYMENT_WAIT_ACCEPT'
    UNKNOWN_STATUS = 'UNKNOWN_STATUS'

    name = models.CharField(max_length=200, default='<no name>')
    surname = models.CharField(max_length=200, default='<no surname>')
    midname = models.CharField(max_length=200, default='<no midname>')
    email = models.EmailField(max_length=200, null=True)
    uid = models.CharField(max_length=200, unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    ticket_type = models.ForeignKey(TicketType)
    status = models.CharField(max_length=25, default=CART_CREATED,
                              choices=((CART_CREATED, 'Item in cart'),
                                       (TICKET_ISSUED, 'Payment confirmed, ticket issued'),
                                       (PAYMENT_FAILED, 'Payment failed'),
                                       (PAYMENT_WAIT_ACCEPT, 'Payment is waiting for acceptance...'),
                                       (UNKNOWN_STATUS, 'Unknown status, check LiqPay data')
                              ))
    ticket = models.ForeignKey(IssuedTicket, null=True, default=None)

    phone_number = models.CharField(max_length=30, blank=True)
    facebook_url = models.URLField(blank=True)
    vk_url = models.URLField(blank=True)
    residence = models.CharField(max_length=200, blank=True)
    working_place = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.uid

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('cart-details', args=[self.uid])


class LiqPayData(models.Model):
    cart = models.ForeignKey(Cart)
    timestamp = models.DateTimeField(auto_now=True, null=True)

    lp_action = models.CharField(max_length=50, null=True)
    lp_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    lp_code = models.CharField(max_length=50, null=True)
    lp_currency = models.CharField(max_length=50, null=True)
    lp_err_code = models.CharField(max_length=50, null=True)
    lp_err_description = models.CharField(max_length=255, null=True)
    lp_ip = models.CharField(max_length=50, null=True)
    lp_liqpay_order_id = models.CharField(max_length=50, null=True)
    lp_payment_id = models.IntegerField(null=True)
    lp_paytype = models.CharField(max_length=50, null=True)
    lp_public_key = models.CharField(max_length=50, null=True)
    lp_sender_card_mask2 = models.CharField(max_length=50, null=True)
    lp_status = models.CharField(max_length=50, null=True)
    lp_transaction_id = models.CharField(max_length=50, null=True)
    lp_type = models.CharField(max_length=50, null=True)


class PromoCode(models.Model):
    uid = models.CharField(max_length=200, unique=True)
    ticket_type = models.ForeignKey(TicketType)
    cart = models.ForeignKey(Cart, null=True)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('promo-details', args=[self.ticket_type.campaign.slug, self.uid])

    def __str__(self):
        return "{} [{}]".format(self.uid, "used" if self.cart else "free")
