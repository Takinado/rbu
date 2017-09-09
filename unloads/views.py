from django.shortcuts import render_to_response

from .models import Unload


def unload_list_view(request):
    context = {'unloads': Unload.objects.all()}
    return render_to_response('unloads/unloads_list_view.html', context)
