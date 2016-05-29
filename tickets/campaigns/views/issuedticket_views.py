from campaigns.models import IssuedTicket
from campaigns.utils.pdf import PDFTemplateView
from campaigns.utils.ticket_utils import do_checkin
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.edit import BaseFormView
from tickets.settings import GOOGLE_MAPS_KEY


class TicketDetailView(DetailView):
    model = IssuedTicket

    def get_slug_field(self):
        return 'uid'

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d.update({'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY})
        return d


class TicketDetailEmailView(TicketDetailView):
    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d.update({'email': True})
        return d


class TicketDetailPDFView(SingleObjectTemplateResponseMixin, BaseDetailView, PDFTemplateView):
    model = IssuedTicket

    def get_slug_field(self):
        return 'uid'

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d.update({'pdf': True, 'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY})
        return d


class CheckInForm(forms.Form):
    uid = forms.CharField()


@method_decorator(login_required, name='post')
class CheckInView(BaseFormView):
    form_class = CheckInForm

    def get_success_url(self):
        return self.ticket.get_absolute_url()

    def form_valid(self, form):
        self.ticket = self.get_ticket(form.cleaned_data['uid'])
        do_checkin(self.ticket)
        return super().form_valid(form)

    def get_ticket(self, uid):
        try:
            ticket = IssuedTicket.objects.get(uid=uid)
        except IssuedTicket.DoesNotExist:
            raise Http404()
        return ticket
