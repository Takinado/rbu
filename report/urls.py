from django.conf.urls import url

from .views import report_index, ajax_test, get_more_tables
from .views import import_csv

urlpatterns = [
    url(r'^$', report_index, name='report_index'),
    # csv
    url(r'^import_csv/$', import_csv, name='import_csv'),
    url(r'^ajax_test/$', ajax_test),
    url(r'^ajax_test2/$', get_more_tables, name='get_more_tables'),
]

# import_csv status_view_day unload_day_create cement_report
# auto_import_csv status_calc_day unload_day_create cement_report
