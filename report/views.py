from django.shortcuts import render

# Create your views here.


def report_index(request):
    return render(request, 'report/index.html')
