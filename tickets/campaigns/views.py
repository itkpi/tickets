import logging
from uuid import uuid4

from campaigns.models import Campaign, TicketType, Cart, IssuedTicket
from django.http import Http404
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django import forms
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from liqpay.liqpay import LiqPay
from tickets.settings import LIQPAY_PUBLIC, LIQPAY_PRIVATE
from campaigns.pdf_views import PDFTemplateView


logger = logging.getLogger(__name__)


class CampaignListView(ListView):
    model = Campaign
    queryset = Campaign.objects.filter(opened=True)


class CampaignDetailView(DetailView):
    model = Campaign


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


class TicketTypeListView(ListView, FormMixin):
    model = TicketType
    form_class = BuyTicketForm

    def dispatch(self, request, *args, **kwargs):
        self.campaign = Campaign.objects.get(slug=self.kwargs['campaign_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return TicketType.objects.filter(campaign=self.campaign).order_by('cost')

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


class TicketDetailView(DetailView):
    model = IssuedTicket

    def get_slug_field(self):
        return 'uid'


class TicketDetailEmailView(TicketDetailView):
    template_name_suffix = '_email'


class TicketDetailPDFView(SingleObjectTemplateResponseMixin, BaseDetailView, PDFTemplateView):
    template_name = 'campaigns/issuedticket_pdf.html'
    model = IssuedTicket

    def get_slug_field(self):
        return 'uid'
