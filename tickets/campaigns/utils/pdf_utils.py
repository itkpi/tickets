from datetime import date
from html import escape

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from weasyprint import HTML


def generate_pdf(body):
    html = HTML(string=body)
    main_doc = html.render()
    pdf = main_doc.write_pdf()
    return pdf


# http://stackoverflow.com/questions/1377446/render-html-to-pdf-in-django-site

class PDFTemplateResponse(TemplateResponse):

    def generate_pdf(self, retval):
        html = self.content

        pdf = generate_pdf(html.decode('utf-8'))
        if pdf:
            self.content = pdf
        else:
            return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
        self['Content-Disposition'] = 'attachment; filename="tedx-kpi-{}-ticket.pdf"'.format(date.today().year)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_post_render_callback(self.generate_pdf)


class PDFTemplateView(TemplateView):
    response_class = PDFTemplateResponse
    content_type = "application/pdf"

