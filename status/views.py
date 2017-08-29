import os
import time
import datetime
import pytz
# import unipath
import simplejson

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DayArchiveView
from django.views.generic.dates import MonthMixin

from rbu import settings

from .forms import ImportForm, ToDoForm
from .models import InVents, OutVents, RbuStatus, Status

import calendar
# Create your views here.


def report_index(request):
    now = datetime.datetime.now()

    c = calendar.HTMLCalendar()
    html_out = c.formatmonth(datetime.datetime.today().year, datetime.datetime.today().month)
    # now.year = '2017'
    # now.month = '7'
    # now.day = '29'

    now = {
        'year': 2017,
        'month': 7,
        'day': 29
    }

    status = Status()
    try:
        status = Status.objects.latest('id')
    except ObjectDoesNotExist:
        print(type(status))

    context = {'status': status, 'now': now, 'calendar': html_out}
    return render(request, 'report/index.html', context)


def char_to_bool(ch):
    if ch == 'C':
        return False
    elif ch == 'O':
        return True
    else:
        return False


def pars(path):
    """
    Импорт csv-файла в базу
    :param path:
    :return:
    """
    f = open(path, 'r')
    i = 0
    c = 0
    e = 0
    status_arr = []
    for line in f:
        i += 1
        line = line[0:-1].split(',')
        status = Status()
        status.date = line[0]
        status.him1 = line[1]
        status.him2 = line[2]
        status.water = line[3]
        status.cement = line[4]
        status.breakstone1 = line[5]
        status.sand = line[6]
        status.breakstone2 = line[7]
        status.img = line[8]
        # x = line[30]
        rbu_status, created = RbuStatus.objects.get_or_create(
            cem_bunker_active=line[27],
            cem_bunker1=line[28],
            cem_bunker2=line[29],
            skip=line[30],
            skip_directions=line[31],
            mixer=line[32]
        )
        # print('rbu ', created)

        in_vents, created = InVents.objects.get_or_create(
            vent1=char_to_bool(line[13]),
            vent2=char_to_bool(line[14]),
            vent3=char_to_bool(line[15]),
            vent4=char_to_bool(line[16]),
            vent5=char_to_bool(line[17]),
            vent6=char_to_bool(line[18]),
            vent7=char_to_bool(line[19]),
            vent8=char_to_bool(line[20]),
            vent9=char_to_bool(line[21]),
            vent10=char_to_bool(line[22]),
            vent11=char_to_bool(line[23]),
            vent12=char_to_bool(line[24]),
            vent13=char_to_bool(line[25]),
            vent14=char_to_bool(line[26]),
            )
        # print('invents ', created, invents)

        out_vents, created = OutVents.objects.get_or_create(
            him=char_to_bool(line[9]),
            water=char_to_bool(line[10]),
            cement=char_to_bool(line[11]),
            composite=not char_to_bool(line[12])
        )

        # time.strptime - делает из строки time.struct_time
        # time.mktime - возвращает timestamp из time.struct_time
        # datetime.fromtimestamp - делает из timestamp datetime

        status, created = Status.objects.get_or_create(
            date=pytz.utc.localize(datetime.datetime.fromtimestamp(time.mktime(time.strptime(line[0],
                                                                                             "%d.%m.%Y %H:%M:%S")))),
            him1=float(line[1]) / 100,
            him2=float(line[2]) / 100,
            water=float(line[3]) / 10,
            cement=float(line[4]) / 10,
            breakstone1=int(line[5]),
            sand=int(line[6]),
            breakstone2=int(line[7]),
            no_error=False if 'e' in line[:30] else True,
            warning=True if line[1] != line[2] or line[5] != line[6] or line[5] != line[7] else False,
            img=line[8],
            vents1=in_vents,
            vents2=out_vents,
            rbu_statuses=rbu_status

        )
        if created:
            c += 1
        if not status.no_error:
            e += 1
            print(line[8])
        status_arr.append([
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
    return render(request, 'status/import.html', context)


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
    return render(request, 'report/get_more_tables.html', {'order': order})


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


def status_day_view(request, year=None, month=None, day=None):
    now = datetime.datetime.now()
    year = '2017'
    month = '7'
    day = '29'
    if not year:
        year = now.year
    if not month:
        month = now.month
    if not day:
        day = now.day
    statuses = Status.objects.filter(
                date__year=year,
                date__month=month,
                date__day=day
            ).order_by('date')
    print(statuses)

    context = {'status_list': statuses,
               }
    return render(request, 'status/status_archive_day.html', context)


def test_page(request):
    if request.method == 'GET':
        form = ToDoForm()
    else:
        form = ToDoForm(request.POST)
    return render(request, "report/template.html", dict(form=form))
