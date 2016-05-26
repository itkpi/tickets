import io
from cgi import escape
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from datetime import date


class PDFTemplateResponse(TemplateResponse):

    def generate_pdf(self, retval):
        html = self.content

        result = io.BytesIO()
        rendering = pisa.CreatePDF(io.StringIO(html.decode('utf-8')), result)

        if rendering.err:
            return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
        else:
            self.content = result.getvalue()
        self['Content-Disposition'] = 'attachment; filename="tedx-kpi-{}-ticket.pdf"'.format(date.today().year)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_post_render_callback(self.generate_pdf)


class PDFTemplateView(TemplateView):
    response_class = PDFTemplateResponse
    content_type = "application/pdf"

# http://stackoverflow.com/questions/1377446/render-html-to-pdf-in-django-site
