from django.contrib import admin

# Register your models here.

from django.contrib.admin import ModelAdmin

from .models import Status, RbuStatus, InVents, OutVents, Unloading, UnloadingType


class StatusAdmin(ModelAdmin):
    # навигация по датам из этого поля
    date_hierarchy = 'date'
    # включенные в форму поля
    # fields = (
    #     ('date1', 'date2'),
    #     'type',
    #     'value1',
    #     'value2',
    #           )
    # фильтры для ManyToManyField
    # filter_horizontal = ('statuses',)
    # filter_vertical = ('statuses',)
    # исключенные из формы поля
    # exclude = ('birth_date',)
    # Указание своего класса формы
    # form = PersonForm
    # Поля выводимые в списке объектов

    list_display = (
        'date',
        'vents1',
        # 'him1',
        # 'water',
        'cement',
        # 'breakstone1',
        # 'sand',
        # 'breakstone2',
        'vents2',
        'rbu_statuses',
        # 'img',
        'no_error'
    )

    # Поля для фильтрации в списке объектов
    # Сильно тормозят, видимо нужны индексы

    list_filter = (
        # 'img',
        # 'vents1',
        'vents2',
        # 'rbu_statuses',
        'no_error',
    )

    # сортировка по
    ordering = ['date', ]
    # записей на странице
    list_per_page = 50
    # поля по которым поиск
    search_fields = ['date', ]

    class Meta:
        model = Status


class RbuStatusAdmin(ModelAdmin):
    list_per_page = 10

    class Meta:
        model = RbuStatus


class InVentsAdmin(ModelAdmin):
    list_per_page = 40

    class Meta:
        model = InVents


class OutVentsAdmin(ModelAdmin):
    class Meta:
        model = OutVents


class UnloadingAdmin(ModelAdmin):
    date_hierarchy = 'date'
    list_display = (
        'date',
        'type',
        'him',
        'water',
        'cement',
        'breakstone',
        'sand',
    )
    ordering = ('date',)

    class Meta:
        model = Unloading


class UnloadingTypeAdmin(ModelAdmin):
    class Meta:
        model = UnloadingType

admin.site.register(Status, StatusAdmin)
admin.site.register(RbuStatus, RbuStatusAdmin)
admin.site.register(InVents, InVentsAdmin)
admin.site.register(OutVents, OutVentsAdmin)
admin.site.register(Unloading, UnloadingAdmin)
admin.site.register(UnloadingType, UnloadingTypeAdmin)
