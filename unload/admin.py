from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Unload, UnloadType, Carrier


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
        model = Unload


class UnloadingTypeAdmin(ModelAdmin):
    class Meta:
        model = UnloadType

admin.site.register(Unload, UnloadingAdmin)
admin.site.register(UnloadType)
admin.site.register(Carrier)
