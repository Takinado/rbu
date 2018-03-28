import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.views.generic import DetailView

from .models import Unload, calculate_all_unloads


def unload_list_view(request):

    # context = {'unloads': []}
    unloads_queryset = Unload.objects.filter(
        datetime=datetime.datetime.now().date()
    )

    context = {'unloads': unloads_queryset}

    if request.GET.keys():
        unloads_queryset = Unload.objects.all()
        if request.GET.get('datetime'):
            unloads_queryset = unloads_queryset.filter(
                datetime=datetime.datetime.strptime(
                    request.GET.get('datetime'),
                    # '%d.%m.%Y'
                    '%Y-%m-%d'
                ).date(),
            )
        context = {'unloads': unloads_queryset}

    return render_to_response('unloads/unloads_list_view.html', context)


def calc_unloads(request):
    calculate_all_unloads()
    return redirect('status_index')


class UnloadDetailView(DetailView):
    model = Unload


def reset_unload_base(request):
    Unload.objects.all().delete()
    return HttpResponseRedirect('/')
