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
