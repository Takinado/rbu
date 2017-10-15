from django.http import HttpResponse
from django.shortcuts import render, render_to_response


def cement_report_form(request):
    # return HttpResponse()
    return render_to_response('reports/cement.html')
