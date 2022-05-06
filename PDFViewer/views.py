import os.path

import pdfkit
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import TemplateView, View


class PDFViewer(TemplateView):
    template_name = "pdf_test.html"

    def get(self, request, *args, **kwargs):
        template = get_template(self.template_name)
        context = dict()
        html = template.render(context)

        tmp_file = "file.pdf"
        pdfkit.from_string(html, tmp_file, {
            'encoding': 'UTF-8',
            'enable-local-file-access': True
        }, css=[])

        file_data = open(tmp_file, "rb").read()

        response = HttpResponse(file_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(tmp_file)}"'
        os.remove(tmp_file)
        return response
