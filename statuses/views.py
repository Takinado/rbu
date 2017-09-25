import os
from datetime import datetime
import simplejson

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import DayArchiveView, DetailView
from django.views.generic.dates import MonthMixin

from rbu import settings

from .forms import ImportForm, ToDoForm
from .models import InVent, OutVent, RbuStatus, Status

import calendar
# Create your views here.


def index_statuses_view(request):
    today = datetime.today().date()
    return redirect('status_list_view', year=today.year, month=today.month, day=today.day)


def report_index(request):
    now = datetime.now()

    c = calendar.HTMLCalendar()
    html_out = c.formatmonth(datetime.today().year, datetime.today().month)
    # now.year = '2017'
    # now.month = '7'
    # now.day = '29'

    now = {
        'year': 2017,
        'month': 8,
        'day': 7
    }

    status = Status()
    try:
        status = Status.objects.latest('id')
    except ObjectDoesNotExist:
        print(type(status))

    context = {'status': status, 'now': now, 'calendar': html_out}
    return render(request, 'reports/index.html', context)


def pars(path):
    """
    Импорт csv-файла в базу
    :param path:
    :return: список строк кратких описаний статусов
    """
    f = open(path, 'r')
    i = 0
    c = 0
    e = 0
    status_arr = []
    for line in f:
        i += 1
        line = line[0:-1].split(',')

        status, created = Status.create(line)

        if created:
            c += 1
        if not status.no_error:
            e += 1
            print(line[8])
        status_arr.append([
            line[0],
            float(line[1]) / 100,
            float(line[2]) / 100,
            float(line[3]) / 10,
            float(line[4]) / 10,
            line[5],
            line[6],
            line[7],
            line[8],
            status.no_error
        ])
    f.close()
    # print status_arr
    return i, c, e, status_arr


def import_one_csv(debug=False):
    """

    :param debug:
    :return: список строк кратких описаний статусов
    """
    statuses = []
    i = 0
    total_n = 0
    total_c = 0
    total_e = 0
    files = os.listdir(os.path.join(settings.MEDIA_ROOT, 'import_in'))
    if files:
        f = files[0]
    # for f in os.listdir(os.path.join(settings.MEDIA_ROOT, 'import_in')):
        if f.endswith('.csv'):
            i += 1
            print(f)
            n, c, e, statuses = pars(os.path.join(settings.MEDIA_ROOT, 'import_in', f))
            total_n += n
            total_c += c
            total_e += e

            if not debug:
                try:
                    pass
                    # path.rename(base.MEDIA_ROOT.child('stat_arh').child(path.name))
                    os.rename(
                        os.path.join(settings.MEDIA_ROOT, 'import_in', f),
                        os.path.join(settings.MEDIA_ROOT, 'import_arh', f),
                    )
                except OSError as exc:
                    print(exc.strerror)

    info = {'reads': total_n, 'inserts': total_c, 'errors': total_e}
    if debug:
        print(info)

    return statuses


def import_csv(request):
    files = os.listdir(os.path.join(settings.MEDIA_ROOT, 'import_in'))
    # files = os.listdir(settings.MEDIA_ROOT.child('import_in'))
    context = {'file': '', 'lines_sum': 0}
    for f in files:
        if f.endswith('.csv'):
            path = f
            lines_sum = sum(1 for l in open(os.path.join(settings.MEDIA_ROOT, 'import_in', f), 'r'))
            # lines_sum = sum(1 for l in open(settings.MEDIA_ROOT.child('import_in').child(f), 'r'))
            context = {'file': f, 'lines_sum': lines_sum, 'remained': len(files)-1}

            # i, c, e, statuses = pars(os.path.join(settings.MEDIA_ROOT, 'stat_in', path))
            #
            # try:
            #     os.rename(
            #         os.path.join(settings.MEDIA_ROOT, 'stat_in', path),
            #         os.path.join(settings.MEDIA_ROOT, 'stat_arh', path)
            #     )
            # except OSError as exc:
            #     print(exc.strerror)
            #
            # print(i, c, e)

    # return render(request, 'betstat/stat_add.html', context)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImportForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cd = form.cleaned_data
            path = cd['file']

            i, c, e, statuses = pars(os.path.join(settings.MEDIA_ROOT, 'import_in', path))
            # i, c, e, statuses = pars(settings.MEDIA_ROOT.child('import_in').child(path))
            context['info'] = {'reads': i, 'inserts': c, 'errors': e}
            context['statuses'] = statuses

            try:
                os.rename(
                    os.path.join(settings.MEDIA_ROOT, 'import_in', path),
                    # settings.MEDIA_ROOT.child('import_in').child(path),
                    os.path.join(settings.MEDIA_ROOT, 'import_arh', path)
                    # settings.MEDIA_ROOT.child('import_arh').child(path)
                )
            except OSError as exc:
                print(exc.strerror)

            # тут бок небольшой
                # TODO не обновляется страница после обработки файла
            return redirect('import_csv')
            # print context
            # redirect to a new URL:
            # return HttpResponse(u'Файл: %s' % (cd['file']))
            # return HttpResponseRedirect('/stat/index/')
            # return render(request, 'betstat/index.html', context)
        # else:
            # context['errors'] = form.errors.as_data()
            # render(request, 'betstat/stat_add.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImportForm(initial={'file': context['file']})
    context['form'] = form
    # print(context)
    return render(request, 'statuses/import.html', context)


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
    queryset = Status.objects.all().select_related('rbu_statuses', 'vents1', 'vents2')\
        .filter(no_error=True)
    date_field = "date"
    ordering = 'date'
    allow_future = True
    month_format = '%m'
    paginate_by = 200
    # template_name = 'report/status_list.html'


def test_page(request):
    if request.method == 'GET':
        form = ToDoForm()
    else:
        form = ToDoForm(request.POST)
    return render(request, "reports/template.html", dict(form=form))


class StatusDetailView(DetailView):
    pass
