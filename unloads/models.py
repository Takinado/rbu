from django.db import models


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
    date = models.DateTimeField(verbose_name='дата')
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
        ordering = ['date', ]
        verbose_name = 'отгрузка'
        verbose_name_plural = 'отгрузки'

    def __str__(self):
        return self.date.strftime("%d.%m.%Y %H:%M:%S")

    def mess(self):
        return 'Отгрузка: %s, Хим: %s, вода: %s, цемент: %s, смесь: %s' % (self,
                                                                           self.him,
                                                                           self.water,
                                                                           self.cement,
                                                                           self.breakstone)


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
