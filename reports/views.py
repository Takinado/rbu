from datetime import datetime

from django.db.models import Sum
from django.shortcuts import redirect
from django.views.generic import MonthArchiveView

from reports.models import Cement


def report_cement_index(request):
    today = datetime.today().date()
    return redirect('report_cement_month', year=today.year, month=today.month)


class CementMonthArchiveView(MonthArchiveView):
    queryset = Cement.objects.all()
    date_field = "date"
    # allow_future = True
    allow_empty = True

    # Добавим в контекст общее кол-во дней
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CementMonthArchiveView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all
        context['total'] = Cement.objects.filter(
            date__year=self.get_year(),
            date__month=self.get_month(),
        ).aggregate(Sum('value'))
        return context

    # Если необходимо обработать какие-то дополнительные параметры из url, то у DetailView(как и у ListView)
    # существуют два свойства: args и kwargs.
    # def get_object(self, **kwargs):
    #     print(self.args)
    #     print(self.kwargs)
    #     return super(PostDetailView, self).get_object(**kwargs)

# def cement_report(request):
#     """
#     Отчет по высыпаному из миксера цементу за период
#     :param request:
#     :return:
#     """
#
#     # cement_report_dict = {}
#     # SELECT
#     # DATE(`date`), SUM(`cement`)
#     # FROM
#     # `rbu_unloading`
#     # GROUP
#     # BY
#     # DATE(`date`)
#
#     # SELECT
#     # DATE(`date`), count(*)
#     # FROM
#     # `rbu_unloading`
#     # WHERE
#     # cement <> 0
#     # GROUP
#     # BY
#     # DATE(`date`);
#
#     context = {}
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = DateForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # cement_query = Unloading.objects.extra(select={'dateuniq': "DATE(`date`)"}) \
#             #     .values('cement', 'dateuniq').order_by() \
#             #     .values('dateuniq').annotate(cement_day=Sum('cement')).filter(
#             #     Q(date__gte=form.cleaned_data['date_start'])
#             #     & Q(date__lte=form.cleaned_data['date_end']))
#
#             cement_query = Unload.objects.extra(select={'dateuniq': "DATE(`date`)"})
#             cement_query = cement_query.values('cement', 'dateuniq').order_by().values('dateuniq')
#             cement_query = cement_query.annotate(cement_day=Sum('cement'))
#
#             cement_query = cement_query.filter(
#                 Q(date__gte=form.cleaned_data['date_start'])
#                 & Q(date__lte=form.cleaned_data['date_end'])
#             ).order_by('dateuniq')
#
#
#
#             # for q in cement_query:
#             #     print(q)
#
#             context = cement_query.aggregate(Sum('cement_day'))
#             context['cement_list'] = cement_query
#
#             # ...
#             # redirect to a new URL:
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = DateForm()
#     context['form'] = form
#     return render(request, 'rbu/cement_report.html', context)
