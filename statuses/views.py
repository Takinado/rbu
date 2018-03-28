import calendar
import os
from datetime import datetime, date

import simplejson
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DayArchiveView, DetailView
from django.views.generic.dates import MonthMixin

from rbu import settings
from unloads.models import Unload
from .forms import ImportForm, ToDoForm
from .models import Status, parsing_csv, calculate_all_statuses


# Create your views here.


def index_statuses_view(request):
    today = datetime.today().date()
    today = date(2018, 1, 21)
    return redirect('status_list_view', year=today.year, month=today.month, day=today.day)


def report_index(request):
    now = datetime.now()

    c = calendar.HTMLCalendar()
    html_out = c.formatmonth(datetime.today().year, datetime.today().month)
    # now.year = '2017'
    # now.month = '7'
    # now.day = '29'

    now = {
        'year': 2018,
        'month': 1,
        'day': 21
    }

    status = Status()
    try:
        status = Status.objects.latest('id')
    except ObjectDoesNotExist:
        print(type(status))

    context = {'status': status, 'now': now, 'calendar': html_out}
    return render(request, 'reports/index.html', context)


def import_csv_view(request):
    context = {'file': '', 'lines_sum': 0}
    files = os.listdir(os.path.join(settings.MEDIA_ROOT, 'import_in'))
    files.sort()
    for f in files[::-1]:
        if f.endswith('.csv'):
            lines_sum = sum(1 for l in open(os.path.join(settings.MEDIA_ROOT, 'import_in', f), 'r'))
            context = {'file': f, 'lines_sum': lines_sum, 'remained': len(files)}

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImportForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cd = form.cleaned_data
            path = cd['file']

            context['info'], context['statuses'] = import_csv(path)

            try:
                os.rename(
                    os.path.join(settings.MEDIA_ROOT, 'import_in', path),
                    os.path.join(settings.MEDIA_ROOT, 'import_arh', path)
                )
            except OSError as exc:
                print(exc.strerror)

            return redirect('import_csv')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImportForm(initial={'file': context['file']})
    context['form'] = form
    return render(request, 'statuses/import.html', context)


def import_csv(filename):
    statuses = []
    status_count = 0
    status_created = 0
    status_errored = 0
    lines = parsing_csv(os.path.join(settings.MEDIA_ROOT, 'import_in', filename))
    for line in lines:
        status, c, e, = Status.create(line)
        status_count += 1
        status_created += c
        status_errored += e
        statuses.append(status)

    info = {'reads': status_count, 'inserts': status_created, 'errors': status_errored}

    return info, statuses


def ajax_test(request):
    results = {'success': False}

    # Тут — потрібні нам алгоритми
    if True:
        results = {'success': True, 'param1': 'Ти таки', 'param2': 'натиснув його!'}

    json = simplejson.dumps(results)
    return HttpResponse(json, content_type='application/json')


# https://stackoverflow.com/questions/34774138/reload-table-data-in-django-without-refreshing-the-page
def get_more_tables(request):
    increment = int(request.GET['append_increment'])
    increment_to = increment + 10
    order = Status.objects.all().order_by('-id')[increment:increment_to]
    return render(request, 'reports/get_more_tables.html', {'order': order})


class StatusDayView(DayArchiveView, MonthMixin):
    # queryset = Status.objects.all()
    queryset = Status.objects.all().select_related('rbu_statuses', 'vents1', 'vents2') \
        .filter(no_error=True)
    date_field = "date"
    ordering = 'time'
    allow_future = True
    month_format = '%m'
    paginate_by = 200
    allow_empty = True
    # template_name = 'report/status_list.html'


def test_page(request):
    if request.method == 'GET':
        form = ToDoForm()
    else:
        form = ToDoForm(request.POST)
    return render(request, "reports/template.html", dict(form=form))


class StatusDetailView(DetailView):
    model = Status


def select_status_day(request):
    """
    Редирект на страницу нужного дня
    :param request:
    :return:
    """
    if 'date' in request.GET:
        date = request.GET['date']
        try:
            d = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return redirect('status_index')
        return redirect('status_list_view', year=d.year, month=d.month, day=d.day)

    # TODO Убрать этот костыль. Сделать Проверку введённых данных - в обработчике формы после MVP
    # ([0-2]\d|3[01])\.(0\d|1[012])\.(\d{4})
    # https://djbook.ru/forum/topic/2471/


def status_month_calc(request, year=None, month=None):
    # def statuses_calc(request):
    for day in range(1, calendar.monthrange(2017, 9)[1] + 1):
        print(day)
        status_day_calc(request, year=year, month=month, day=day)
    return redirect('status_index')


def status_day_calc(request, year=None, month=None, day=None):
    """
    Расчет параметров статусов дня
    :param request:
    :param year:
    :param month:
    :param day:
    :return:
    """
    if day is None:
        status_list_full = Status.objects.select_related('rbu_statuses', 'vents1', 'vents2').filter(
            date__year=year,
            date__month=month
        ).order_by('date')
    else:
        status_list_full = Status.objects.select_related('rbu_statuses', 'vents1', 'vents2').filter(
            date__year=year,
            date__month=month,
            date__day=day
        ).order_by('date')
    error_count = status_list_full.filter(no_error=False).count()
    status_list = status_list_full.filter(no_error=True).order_by('date')

    if len(status_list) >= 1:
        for status in status_list:
            status.calculate_status()

    context = {'status_list': status_list,
               'error_count': error_count,
               'title': 'Расчет статусов за день'
               }
    return render(request, 'statuses/status_archive_day.html', context)


def calc_statuses(request):
    # status_list_full = Status.objects.select_related('rbu_statuses', 'vents1', 'vents2').order_by('date')
    # error_count = status_list_full.filter(no_error=False).count()
    # status_list = status_list_full.filter(no_error=True).order_by('date')
    calculate_all_statuses()
    return redirect('status_index')


def reset_base(request):
    Unload.objects.all().delete()
    Status.objects.all().delete()
    return HttpResponseRedirect('/')
