from django.conf.urls import url

# from .views import cement_report_form, CementMonthArchiveView, report_cement_index
from .views import CementMonthArchiveView, report_cement_index

urlpatterns = [
    # url(r'^$', unload_list_view, name='report_index'),
    # url(r'^cement/$', cement_report_form, name='report_cement'),

    url(r'^cement/$', report_cement_index, name='report_cement_index'),
    # Example: /2012/08/
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        CementMonthArchiveView.as_view(month_format='%m'),
        name="report_cement_month"),
]
