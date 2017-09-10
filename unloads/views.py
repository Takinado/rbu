import datetime

from django.shortcuts import render_to_response

from .models import Unload


def unload_list_view(request):

    # context = {'unloads': []}
    unloads_queryset = Unload.objects.filter(
        date=datetime.datetime.now().date()
    )

    context = {'unloads': unloads_queryset}

    if request.GET.keys():
        unloads_queryset = Unload.objects.all()
        if request.GET.get('date'):
            unloads_queryset = unloads_queryset.filter(
                date = datetime.datetime.strptime(
                    request.GET.get('date'),
                    '%d.%m.%Y'
                ).date(),
            )
        context = {'unloads': unloads_queryset}

    return render_to_response('unloads/unloads_list_view.html', context)
