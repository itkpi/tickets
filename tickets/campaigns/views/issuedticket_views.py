from campaigns.models import IssuedTicket
from campaigns.utils.email_utils import notify_owner
from campaigns.utils.pdf_utils import PDFTemplateView
from campaigns.utils.ticket_utils import do_checkin
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.edit import BaseFormView
from django.shortcuts import redirect
from tickets.settings import GOOGLE_MAPS_KEY


class TicketDetailView(DetailView):
    model = IssuedTicket

    def get_slug_field(self):
        return 'uid'

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d.update({'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY})
        return d

    def get(self, request, **kwargs):
        r = super().get(request, **kwargs)
        if self.object.alias_for:
            ticket = IssuedTicket.objects.get(uid=self.object.alias_for)
            return redirect(ticket.get_absolute_url())
        return r


class TicketDetailEmailView(TicketDetailView):
    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d.update({'email': True})
        return d


class TicketDetailPDFHTMLView(SingleObjectTemplateResponseMixin, BaseDetailView, TemplateView):
    template_name_suffix = '_pdf'
    model = IssuedTicket

    def get_slug_field(self):
        return 'uid'

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d.update({'pdf': True, 'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY})
        return d

    def get(self, request, **kwargs):
        r = super().get(request, **kwargs)
        if self.object.alias_for:
            ticket = IssuedTicket.objects.get(uid=self.object.alias_for)
            return redirect(ticket.get_absolute_url())
        return r


class TicketDetailPDFView(TicketDetailPDFHTMLView, PDFTemplateView):
    pass


class TicketForm(forms.Form):
    uid = forms.CharField()


class TicketActionView(BaseFormView):
    form_class = TicketForm

    def get_success_url(self):
        return self.ticket.get_absolute_url()

    def form_valid(self, form):
        self.ticket = self.get_ticket(form.cleaned_data['uid'])
        self.ticket_action(self.ticket)
        return super().form_valid(form)

    def get_ticket(self, uid):
        try:
            ticket = IssuedTicket.objects.get(uid=uid)
        except IssuedTicket.DoesNotExist:
            raise Http404()
        return ticket

    def ticket_action(self, ticket):
        raise NotImplementedError()


@method_decorator(login_required, name='post')
class CheckInView(TicketActionView):
    def ticket_action(self, ticket):
        do_checkin(ticket)


class TicketEmailSendView(TicketActionView):
    def ticket_action(self, ticket):
        notify_owner(ticket)
