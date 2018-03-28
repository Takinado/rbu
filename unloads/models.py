from django.db import models

from statuses.models import Status


class UnloadType(models.Model):
    name = models.CharField(max_length=127, default='Новый тип отгрузки', verbose_name='имя')
    description = models.TextField(blank=True, verbose_name='Описание')
    him = models.FloatField(default=0, verbose_name='химия')
    water = models.FloatField(default=0, verbose_name='вода')
    cement = models.FloatField(default=0, verbose_name='цемент')
    breakstone = models.PositiveSmallIntegerField(default=0, verbose_name='щебень')
    sand = models.PositiveSmallIntegerField(default=0, verbose_name='песок')

    average_him = models.FloatField(default=0, verbose_name='химия в среднем')
    average_water = models.FloatField(default=0, verbose_name='вода в среднем')
    average_cement = models.FloatField(default=0, verbose_name='цемент в среднем')
    average_breakstone = models.PositiveSmallIntegerField(default=0, verbose_name='щебень в среднем')
    average_sand = models.PositiveSmallIntegerField(default=0, verbose_name='песок в среднем')

    class Meta:
        verbose_name = 'тип отгрузки'
        verbose_name_plural = 'типы отгрузок'

    def __str__(self):
        # return self.name.encode('utf8')
        return self.name


class Unload(models.Model):
    datetime = models.DateTimeField(verbose_name='дата', db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(UnloadType, blank=True, null=True, verbose_name='тип')
    value = models.FloatField(null=True, default=None, verbose_name='объем')
    him = models.FloatField(default=0, verbose_name='химия')
    water = models.FloatField(default=0, verbose_name='вода')
    cement = models.FloatField(default=0, verbose_name='цемент')
    breakstone = models.SmallIntegerField(default=0, verbose_name='щебень')
    sand = models.SmallIntegerField(default=0, verbose_name='песок')
    is_active_left_bunker = models.NullBooleanField(null=True, blank=True, verbose_name='активный бункер - левый')
    carrier = models.ForeignKey('Carrier', blank=True, default=None, null=True, verbose_name='Машина')

    class Meta:
        ordering = ['datetime', ]
        verbose_name = 'отгрузка'
        verbose_name_plural = 'отгрузки'

    def __str__(self):
        return self.datetime.strftime("%d.%m.%Y %H:%M:%S")

    def mess(self):
        return 'Отгрузка: {}, Хим: {}, вода: {}, цемент: {}, смесь: {}'.format(
            self,
            self.him,
            self.water,
            self.cement,
            self.breakstone
        )


def calculate_all_unloads():
    start_status = Status.objects.filter(unload=None).earliest('datetime')
    end_status = Status.objects.latest('datetime')
    calculate_unloads(start_status, end_status)
    return


def calculate_unloads(start_status, end_status):
    print(start_status, end_status)
    statuses_for_unload = []
    uncalculated_statuses = Status.objects.filter(
        no_error=True,
        datetime__gte=start_status.datetime,
        datetime__lte=end_status.datetime
    ).order_by('datetime')
    print(uncalculated_statuses.count())
    for status in uncalculated_statuses:
        statuses_for_unload.append(status)
        if status.is_status_end_unload():
            create_unload(statuses_for_unload)
            print(statuses_for_unload[-1])
        # else:
        #     statuses_for_unload.append(status)
    return


def create_unload(statuses_for_unload):
    prev_status = statuses_for_unload[-1].get_previous()

    unload, created = Unload.objects.get_or_create(
        datetime=statuses_for_unload[-1].datetime,
    )
    # unload.date = status.date
    unload.him = prev_status.mix_him
    unload.water = prev_status.mix_water
    unload.cement = prev_status.mix_cement
    unload.breakstone = prev_status.mix_breakstone
    unload.sand = prev_status.mix_sand
    unload.is_active_left_bunker = True if prev_status.rbu_statuses.cem_bunker_active == 'L' else False
    unload.save()
    for status in statuses_for_unload:
        status.unload = unload
        status.save()
    return


class CarrierManager(models.Manager):
    def create_carrier(self, unload_list):
        date = unload_list[0].date

        carrier = self.create(date=date)
        # do something with the carrier
        return carrier


class Carrier(models.Model):
    date = models.DateTimeField(verbose_name='дата')
    type = models.ForeignKey(UnloadType, blank=True, null=True, verbose_name='тип')
    value = models.FloatField(default=1, verbose_name='объем')
    him = models.FloatField(default=0, verbose_name='химия')
    water = models.FloatField(default=0, verbose_name='вода')
    cement = models.FloatField(default=0, verbose_name='цемент')
    breakstone = models.SmallIntegerField(default=0, verbose_name='щебень')
    sand = models.SmallIntegerField(default=0, verbose_name='песок')

    objects = CarrierManager()

    class Meta:
        ordering = ['date', ]
        verbose_name = 'Машина'
        verbose_name_plural = 'машины'

    def __str__(self):
        return self.date.strftime("%d.%m.%Y %H:%M:%S")
