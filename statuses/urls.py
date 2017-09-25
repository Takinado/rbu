from django.conf.urls import url

from .views import index_statuses_view, test_page
from .views import ajax_test, get_more_tables
from .views import StatusDayView
from .views import import_csv

urlpatterns = [
    # url(r'^$', unload_list_view, name='report_index'),
    url(r'^$', index_statuses_view, name='status_index'),
    # csv
    url(r'^import_csv/$', import_csv, name='import_csv'),
    url(r'^ajax_test/$', ajax_test),
    url(r'^ajax_test2/$', get_more_tables, name='get_more_tables'),

    # url(r'^status_list/$', status_day_view, name="status_list"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        StatusDayView.as_view(),
        name="status_list_view"),

    url(r'^test/$', test_page),
]

# import_csv status_view_day unload_day_create cement_report
# auto_import_csv status_calc_day unload_day_create cement_report
