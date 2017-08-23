from django.db import models

# Create your models here.


class InVents(models.Model):
    # name = models.CharField(max_length=127, blank=True, null=True, verbose_name='имя')
    vent1 = models.BooleanField(verbose_name='химия1')
    vent2 = models.BooleanField(verbose_name='химия2')
    vent3 = models.BooleanField(verbose_name='химия3')
    vent4 = models.BooleanField(verbose_name='химия4')
    vent5 = models.BooleanField(verbose_name='вода1')
    vent6 = models.BooleanField(verbose_name='вода2')
    vent7 = models.BooleanField(verbose_name='цемент1')
    vent8 = models.BooleanField(verbose_name='цемент2')
    vent9 = models.BooleanField(verbose_name='щебень1')
    vent10 = models.BooleanField(verbose_name='щебень2')
    vent11 = models.BooleanField(verbose_name='песок1')
    vent12 = models.BooleanField(verbose_name='песок2')
    vent13 = models.BooleanField(verbose_name='щебень3')
    vent14 = models.BooleanField(verbose_name='щебень4')

    # def __str__(self):
    #     if self.name:
    #         return self.name
    #     else:
    #         return 'new'

    def is_him_in(self):
        return self.vent1 or self.vent2 or self.vent3 or self.vent4

    def is_water_in(self):
        return self.vent5 or self.vent6

    def is_cement_in(self):
        return self.vent7 or self.vent8

    def is_breakstone_in(self):
        return self.vent9 or self.vent10 or self.vent13 or self.vent14

    def is_sand_in(self):
        return self.vent11 or self.vent12

    class Meta:
        verbose_name = 'состояние наполнительных вентилей'
        verbose_name_plural = 'состояния наполнительных вентилей'


class OutVents(models.Model):
    name = models.CharField(max_length=127, blank=True, null=True, verbose_name='имя')
    him = models.BooleanField(verbose_name='химия')
    water = models.BooleanField(verbose_name='вода')
    cement = models.BooleanField(verbose_name='цемент')
    composite = models.BooleanField(verbose_name='смесь')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.him) + ';' + str(self.water) + ';' + str(self.cement) + ';' + str(self.composite)

    class Meta:
        verbose_name = 'состояние выпускных вентилей'
        verbose_name_plural = 'состояние выпускных вентилей'


class RbuStatus(models.Model):
    BUNKER_STATUS_CHOICES = (
        ('F', 'Полный'),
        ('H', 'Полупустой'),
        ('N', 'Пустой'),
        ('e', 'ОШИБКА'),
    )
    BUNKER_CHOICES = (
        ('L', 'Левый'),
        ('R', 'Правый'),
        ('e', 'ОШИБКА'),
    )
    SKIP_STATUS_CHOICES = (
        ('F', 'Полный'),
        ('N', 'Пустой'),
        ('e', 'ОШИБКА'),
    )
    SKIP_DIRECTIONS_CHOICES = (
        ('U', 'Вверх быстро'),
        ('M', 'Вверх'),
        # ('S', 'Стоит'),
        ('D', 'Вниз'),
        ('e', 'ОШИБКА'),
    )
    MIXER_STATUS_CHOICES = (
        ('C', 'Закрыт'),
        ('M', 'Изменяется'),
        ('O', 'Открыт'),
        ('e', 'ОШИБКА'),
    )

    name = models.CharField(max_length=127, blank=True, null=True, verbose_name='имя')
    cem_bunker_active = models.CharField(max_length=1, choices=BUNKER_CHOICES, verbose_name='активный бункер')
    cem_bunker1 = models.CharField(max_length=1, choices=BUNKER_STATUS_CHOICES, verbose_name='первый бункер')
    cem_bunker2 = models.CharField(max_length=1, choices=BUNKER_STATUS_CHOICES, verbose_name='второй бункер')
    skip = models.CharField(max_length=1, choices=SKIP_STATUS_CHOICES, verbose_name='Скип')
    skip_directions = models.CharField(max_length=1, choices=SKIP_DIRECTIONS_CHOICES, verbose_name='скип движется')
    mixer = models.CharField(max_length=1, choices=MIXER_STATUS_CHOICES, verbose_name='выпускной тракт')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ';'.join([self.cem_bunker_active,
                             self.cem_bunker1,
                             self.cem_bunker2,
                             self.skip,
                             self.skip_directions,
                             self.mixer
                             ])

    class Meta:
        verbose_name = 'состояние блоков'
        verbose_name_plural = 'состояния блоков'


# class StatusManager(models.Manager):
#
#     use_for_related_fields = True
#
#     def errored(self, **kwargs):
#         return self.filter(no_error=False, **kwargs)


class Status(models.Model):
    # name = models.CharField(max_length=127, blank=True, null=True, verbose_name='имя')
    date = models.DateTimeField(verbose_name='дата')
    him1 = models.FloatField(verbose_name='химия1')
    him2 = models.FloatField(verbose_name='химия2')
    water = models.FloatField(verbose_name='вода')
    cement = models.FloatField(verbose_name='цемент')
    breakstone1 = models.PositiveSmallIntegerField(verbose_name='щебень1')
    sand = models.PositiveSmallIntegerField(verbose_name='песок')
    breakstone2 = models.PositiveSmallIntegerField(verbose_name='щебень2')
    img = models.ImageField(verbose_name='картинка')
    no_error = models.BooleanField(default=False, verbose_name='без ошибок')

    vents1 = models.ForeignKey(InVents, verbose_name='Впускные вентили')
    vents2 = models.ForeignKey(OutVents, verbose_name='Выпускные вентили')
    rbu_statuses = models.ForeignKey(RbuStatus, verbose_name='Состояние блоков')
    warning = models.BooleanField(default=False, verbose_name='Предупреждение')

    mix_him = models.FloatField(default=0, verbose_name='химия в миксере')
    mix_water = models.FloatField(default=0, verbose_name='вода в миксере')
    mix_cement = models.FloatField(default=0, verbose_name='цемент в миксере')
    mix_breakstone = models.SmallIntegerField(default=0, verbose_name='щебень в миксере')
    mix_sand = models.SmallIntegerField(default=0, verbose_name='песок в миксере')
    skip_breakstone = models.SmallIntegerField(default=0, verbose_name='щебень в скипе')
    skip_sand = models.SmallIntegerField(default=0, verbose_name='песок в скипе')
    storage_breakstone = models.SmallIntegerField(default=0, verbose_name='щебень в накопителе')
    storage_sand = models.SmallIntegerField(default=0, verbose_name='песок в накопителе')
    unload = models.ForeignKey('Unloading', blank=True, null=True, verbose_name='Выгрузка')
    is_processed = models.BooleanField(default=False, verbose_name='Обработан')

    # add our custom model manager
    # objects = StatusManager()

    def get_value(self, num):
        if num == 1 or num == 6:
            return self.him1
        elif num == 2 or num == 7:
            return self.water
        elif num == 3 or num == 8:
            return self.cement
        elif num == 4 or num == 9:
            return self.breakstone1
        elif num == 5:
            return self.sand
        else:
            return 0

    def is_change(self, num):
        if num == 1:
            return self.vents1.is_him_in()
        elif num == 2:
            return self.vents1.is_water_in()
        elif num == 3:
            return self.vents1.is_cement_in()
        elif num == 4:
            return self.vents1.is_breakstone_in()
        elif num == 5:
            return self.vents1.is_sand_in()
        elif num == 6:
            return self.vents2.him
        elif num == 7:
            return self.vents2.water
        elif num == 8:
            return self.vents2.cement
        elif num == 9:
            return self.vents2.composite
        elif num == 10:
            return self.rbu_statuses.skip
        elif num == 11:
            return self.rbu_statuses.mixer
        else:
            return 0

    @property
    def get_img_shortname(self):
        return self.img.path.split('\\')[-1]

    @property
    def is_mix_empty(self):
        if 0 != self.mix_him or 0 != self.mix_water or 0 != self.mix_cement:
            return False
        if 0 != self.mix_breakstone or 0 != self.mix_sand:
            return False
        return True

    def __str__(self):
        return self.date.strftime("%d.%m.%Y %H:%M:%S")

    class Meta:
        ordering = ['-date', ]
        verbose_name = 'статус РБУ'
        verbose_name_plural = 'статусы РБУ'


class UnloadingType(models.Model):
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


class Unloading(models.Model):
    date = models.DateTimeField(verbose_name='дата')
    type = models.ForeignKey(UnloadingType, blank=True, null=True, verbose_name='тип')
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
    type = models.ForeignKey(UnloadingType, blank=True, null=True, verbose_name='тип')
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


class LoadBunker(models.Model):
    status_prev = models.ForeignKey(Status, verbose_name='Статус ДО', related_name="status_prev")
    status_curr = models.ForeignKey(Status, verbose_name='Статус ПОСЛЕ', related_name="status_curr")
    value = models.PositiveSmallIntegerField(default=30, verbose_name='Задуто')
    is_valid = models.BooleanField(default=False, verbose_name='Подтверждена')

    def __str__(self):
        return self.status_curr.date.strftime("%d.%m.%Y %H:%M:%S")

    class Meta:
        unique_together = ("status_prev", "status_curr")
