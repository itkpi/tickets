import logging
from uuid import uuid4

from campaigns.models import TicketType, Campaign, Cart
from django import forms
from django.db.models import Count, Q, F
from django.http import Http404
from django.shortcuts import redirect
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views.generic import ListView
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


def available_tickettypes_queryset(campaign):
    filter = TicketType.objects. \
        filter(campaign=campaign). \
        filter(public=True). \
        annotate(issued_amount=Count('issuedticket')). \
        filter(Q(unlimited=True) | Q(unlimited=False, amount__gt=F('issued_amount'))). \
        filter(Q(available_from__isnull=True) | Q(available_from__isnull=False, available_from__lt=now())). \
        filter(Q(available_till__isnull=True) | Q(available_till__isnull=False, available_till__gt=now())). \
        order_by('cost')
    return filter


class TicketTypeListView(ListView, FormMixin):
    model = TicketType
    form_class = BuyTicketForm

    def dispatch(self, request, *args, **kwargs):
        self.campaign = Campaign.objects.get(slug=self.kwargs['campaign_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        filter = available_tickettypes_queryset(self.campaign)
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

            cart = Cart(uid="CART-{}".format(uuid4()),
                        ticket_type=tickettype,
                        **data)
            cart.save()
            logger.info('Ticket {} added to cart {}'.format(tickettype, cart))
            return redirect(cart.get_absolute_url())
        else:
            return self.get(request, *args, **kwargs)
