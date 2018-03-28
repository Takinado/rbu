import csv
from datetime import datetime

from django.db import models


class InVent(models.Model):
    name = models.CharField(max_length=127, blank=True, null=True, verbose_name='имя')
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
    description = models.TextField(blank=True, null=True, verbose_name='описание')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return 'Состояние #{}'.format(self.pk)

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


class OutVent(models.Model):
    name = models.CharField(max_length=127, blank=True, null=True, verbose_name='имя')
    him = models.BooleanField(verbose_name='химия')
    water = models.BooleanField(verbose_name='вода')
    cement = models.BooleanField(verbose_name='цемент')
    composite = models.BooleanField(verbose_name='смесь')
    description = models.TextField(blank=True, null=True, verbose_name='описание')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return '{};{};{};{}'.format(
                str(self.him),
                str(self.water),
                str(self.cement),
                str(self.composite)
            )

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
    description = models.TextField(blank=True, null=True, verbose_name='описание')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return '{}{}{} {}{} {}'.format(
                self.cem_bunker_active,
                self.cem_bunker1,
                self.cem_bunker2,
                self.skip,
                self.skip_directions,
                self.mixer
            )

    class Meta:
        verbose_name = 'состояние блоков'
        verbose_name_plural = 'состояния блоков'


# class StatusManager(models.Manager):
#
#     use_for_related_fields = True
#
#     def errored(self, **kwargs):
#         return self.filter(no_error=False, **kwargs)


def char_to_bool(ch):
    if ch == 'C':
        return False
    elif ch == 'O':
        return True
    else:
        return False


def parsing_csv(path):
    lines = []
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            lines.append(row)
    return lines


def create_img_name(path):
    return path.split('\\')[-1][:-4]


class Status(models.Model):
    datetime = models.DateTimeField(verbose_name='дата', db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    date = models.DateField(verbose_name='дата')
    time = models.TimeField(verbose_name='время')
    him1 = models.FloatField(verbose_name='химия1')
    him2 = models.FloatField(verbose_name='химия2')
    water = models.FloatField(verbose_name='вода')
    cement = models.FloatField(verbose_name='цемент')
    breakstone1 = models.PositiveSmallIntegerField(verbose_name='щебень1')
    sand = models.PositiveSmallIntegerField(verbose_name='песок')
    breakstone2 = models.PositiveSmallIntegerField(verbose_name='щебень2')
    img = models.ImageField(verbose_name='картинка')
    no_error = models.BooleanField(default=False, verbose_name='без ошибок')

    vents1 = models.ForeignKey(InVent, verbose_name='Впускные вентили')
    vents2 = models.ForeignKey(OutVent, verbose_name='Выпускные вентили')
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
    unload = models.ForeignKey('unloads.Unload', blank=True, null=True, verbose_name='Выгрузка')
    is_processed = models.BooleanField(default=False, verbose_name='Обработан')

    get_latest_by = 'datetime'

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

    @staticmethod
    def create(line):
        status = Status()
        status.date = datetime.strptime(line[0].split()[0], '%d.%m.%Y').date()
        status.time = datetime.strptime(line[0].split()[1], '%H:%M:%S').time()
        status.datetime = datetime.combine(status.date, status.time)
        status.him1 = line[1]
        status.him2 = line[2]
        status.water = line[3]
        status.cement = line[4]
        status.breakstone1 = line[5]
        status.sand = line[6]
        status.breakstone2 = line[7]
        status.img = create_img_name(line[8])

        rbu_status, created = RbuStatus.objects.get_or_create(
            cem_bunker_active=line[27],
            cem_bunker1=line[28],
            cem_bunker2=line[29],
            skip=line[30],
            skip_directions=line[31],
            mixer=line[32]
        )

        in_vents, created = InVent.objects.get_or_create(
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

        out_vents, created = OutVent.objects.get_or_create(
            him=char_to_bool(line[9]),
            water=char_to_bool(line[10]),
            cement=char_to_bool(line[11]),
            composite=not char_to_bool(line[12])
        )

        created_status, created = Status.objects.get_or_create(
            datetime=status.datetime,
            date=status.date,
            time=status.time,
            him1=float(line[1]) / 100,
            him2=float(line[2]) / 100,
            water=float(line[3]) / 10,
            cement=float(line[4]) / 10,
            breakstone1=int(line[5]),
            sand=int(line[6]),
            breakstone2=int(line[7]),
            no_error=False if 'e' in line[:30] else True,
            warning=True if line[1] != line[2] or line[5] != line[6] or line[5] != line[7] else False,
            img=create_img_name(line[8]),
            vents1=in_vents,
            vents2=out_vents,
            rbu_statuses=rbu_status
        )
        return created_status, created, not created_status.no_error

    @property
    def get_img_shortname(self):
        return '{}.jpg'.format(self.img.path)

    @property
    def is_mix_empty(self):
        if self.mix_him != 0 or self.mix_water != 0 or self.mix_cement != 0:
            return False
        if self.mix_breakstone != 0 or self.mix_sand != 0:
            return False
        return True

    def get_previous(self):
        # https://docs.djangoproject.com/en/1.11/ref/models/instances/#django.db.models.Model.get_previous_by_FOO
        try:
            previous_status = self.get_previous_by_datetime()
        except Status.DoesNotExist:
            return self
        return previous_status

    def calculate_status(self):
        """
        Вычисление параметров статуса
        """
        prev_status = self.get_previous()
        # Химию в миксер
        if self.vents2.him or prev_status.vents2.him:
            self.mix_him = round(prev_status.him1 - self.him1 + prev_status.mix_him, 2)
        else:
            self.mix_him = prev_status.mix_him
        # Воду в миксер
        if self.vents2.water or prev_status.vents2.water:
            self.mix_water = round(prev_status.water - self.water + prev_status.mix_water, 2)
        else:
            self.mix_water = prev_status.mix_water
        # Цемент в миксер
        if self.vents2.cement or prev_status.vents2.cement:
            self.mix_cement = round(prev_status.cement - self.cement + prev_status.mix_cement, 2)
        else:
            self.mix_cement = prev_status.mix_cement
        # Смесь в скип
        if prev_status.vents2.composite:

            delta = prev_status.breakstone1 - self.breakstone1
            self.skip_breakstone = prev_status.skip_breakstone + delta
        else:
            self.skip_breakstone = prev_status.skip_breakstone
        # Скип в миксер
        if self.rbu_statuses.skip == 'N' and prev_status.rbu_statuses.skip == 'F':
            self.mix_breakstone = prev_status.mix_breakstone + self.skip_breakstone
            self.skip_breakstone = 0
        else:
            self.mix_breakstone = prev_status.mix_breakstone
        # Выгрузка
        if self.find_unload_in_statuses():
            self.mix_him = self.mix_water = self.mix_cement = self.mix_breakstone = self.mix_sand = 0

        self.is_processed = True
        self.save()
        return

    def find_unload_in_statuses(self):
        """
        Поиск отгрузки
        """
        prev_status = self.get_previous()
        if self.rbu_statuses.mixer == 'O' and prev_status.rbu_statuses.mixer != 'O':
            if not prev_status.is_mix_empty:
                return True
        return False

    def __str__(self):
        return '{} {}'.format(self.date.strftime("%d.%m.%Y"), self.time.strftime("%H:%M:%S"))

    class Meta:
        ordering = ['-datetime', ]
        verbose_name = 'статус РБУ'
        verbose_name_plural = 'статусы РБУ'


def count_uncalculated_statuses():
    statuses = Status.objects.filter(is_processed=False).count()
    return statuses


def calculate_all_statuses():
    start_status = Status.objects.filter(is_processed=False).earliest('datetime')
    end_status = Status.objects.latest('datetime')
    calculate_statuses(start_status, end_status)
    return


def calculate_statuses(start_status, end_status):
    uncalculated_statuses = Status.objects.filter(
        datetime__gte=start_status.datetime,
        datetime__lte=end_status.datetime
    )
    for status in uncalculated_statuses:
        status.calculate_status()
    return


class LoadBunker(models.Model):
    status_prev = models.ForeignKey(Status, verbose_name='Статус ДО', related_name="status_prev")
    status_curr = models.ForeignKey(Status, verbose_name='Статус ПОСЛЕ', related_name="status_curr")
    value = models.PositiveSmallIntegerField(default=30, verbose_name='Задуто')
    is_valid = models.BooleanField(default=False, verbose_name='Подтверждена')

    def __str__(self):
        return self.status_curr.date.strftime("%d.%m.%Y")

    class Meta:
        unique_together = ("status_prev", "status_curr")
