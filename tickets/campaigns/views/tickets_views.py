import logging
from uuid import uuid4

from campaigns.models import TicketType, Campaign, Cart, PromoCode
from django import forms
from django.db.models import Count, Q, F
from django.http import Http404
from django.shortcuts import redirect, render_to_response
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

logger = logging.getLogger(__name__)


class BuyTicketForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    midname = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.RegexField(regex=r'^\d{9,15}$', error_messages={'invalid': "Phone number must be entered in the format: '380501234567'. Up to 15 digits allowed."})
    facebook_url = forms.URLField(required=False)
    vk_url = forms.URLField(required=False)
    residence = forms.CharField()
    working_place = forms.CharField(required=False)

    submit = forms.IntegerField()


def present_tickettypes_queryset(request, campaign):
    return TicketType.objects. \
        filter(campaign=campaign). \
        annotate(issued_amount=Count('counter__tickettype__issuedticket', distinct=True)). \
        filter(Q(counter__isnull=True) |
               (Q(counter__isnull=False) & (Q(counter__unlimited=True) |
                                            Q(counter__unlimited=False, counter__amount__gt=F('issued_amount'))))). \
        filter(Q(available_from__isnull=True) | Q(available_from__isnull=False, available_from__lt=now())). \
        filter(Q(available_till__isnull=True) | Q(available_till__isnull=False, available_till__gt=now()))


def available_tickettypes_queryset(request, campaign):
    filter = present_tickettypes_queryset(request, campaign). \
        order_by('cost')
    if not request.user.is_superuser:
        filter = filter.filter(public=True)
    return filter


class TicketTypeListView(ListView, FormMixin):
    model = TicketType
    form_class = BuyTicketForm

    def dispatch(self, request, *args, **kwargs):
        self.campaign = Campaign.objects.get(slug=self.kwargs['campaign_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        filter = available_tickettypes_queryset(self.request, self.campaign)
        return filter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'campaign': self.campaign})
        return context

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            tickettype = TicketType.objects.get(id=form.cleaned_data['submit'])
            data = form.cleaned_data.copy()
            del data['submit']

            cart = self.create_cart(data, tickettype)
            logger.info('Ticket {} added to cart {}'.format(tickettype, cart))
            return redirect(cart.get_absolute_url())
        else:
            return self.get(request, *args, **kwargs)

    def create_cart(self, data, tickettype):
        cart = Cart(uid="CART-{}".format(uuid4()),
                    ticket_type=tickettype,
                    **data)
        cart.save()
        return cart


class PromoDetailView(TicketTypeListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.promocode = PromoCode.objects.get(uid=self.kwargs['promo_uid'])
        except PromoCode.DoesNotExist:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.promocode.cart is not None:
            return redirect(self.promocode.cart.get_absolute_url())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        filter = TicketType.objects.filter(id=self.promocode.ticket_type.id)
        return filter

    def create_cart(self, data, tickettype):
        cart = super().create_cart(data, tickettype)
        self.promocode.cart = cart
        self.promocode.save()
        return cart
