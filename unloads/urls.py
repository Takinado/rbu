from django.conf.urls import url

from unloads.views import (
    unload_list_view,
    UnloadDetailView,
    calc_unloads,
)

urlpatterns = [
    url(r'^$', unload_list_view, name="unload_list"),
    url(r'^(?P<pk>\d+)/$', UnloadDetailView.as_view(), name="unload_detail"),
    url(r'^calc/$', calc_unloads, name='calc_unloads'),
]
