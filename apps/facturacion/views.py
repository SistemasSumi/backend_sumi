from django.shortcuts import render

from django.views.generic import TemplateView,View
from django.http import HttpResponse
# Create your views here.


# class ReporteFactura(TemplateView):
#     template_name = "factura.html"
    

# class ReporteFactura(View):
#     template_name = "factura.html"

#     def get(self, request,*args, **kwargs):
#         pdf = render_to_pdf("factura.html",{
#                 'pagesize':'A4',
#                 'mylist': None,
#             })
#         return HttpResponse(pdf,content_type="application/pdf")

# def myview(request):
#     Retrieve data or whatever you need
#     return render_to_pdf(
#             'mytemplate.html',
#             {
#                 'pagesize':'A4',
#                 'mylist': results,
#             }
#         )
