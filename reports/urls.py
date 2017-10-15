from django.conf.urls import url

from .views import cement_report_form

urlpatterns = [
    # url(r'^$', unload_list_view, name='report_index'),
    url(r'^cement/$', cement_report_form, name='report_cement'),
]

# import_csv status_view_day unload_day_create cement_report
# auto_import_csv status_calc_day unload_day_create cement_report
