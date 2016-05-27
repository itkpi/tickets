from campaigns.models import IssuedTicket
from campaigns.utils.pdf import PDFTemplateView
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView


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
