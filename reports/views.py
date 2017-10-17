from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
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
