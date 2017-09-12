from django.conf.urls import url

from unloads.views import unload_list_view, UnloadDetailView

urlpatterns = [
    url(r'^$', unload_list_view, name="unload_list"),
    url(r'^(?P<pk>\d+)/$', UnloadDetailView.as_view(), name="unload_detail"),
    # url(r'^status_list/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
    #     StatusDayView.as_view(),
    #     name="status_list_view"),
]
