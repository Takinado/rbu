from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Unload, UnloadType, Carrier


# class UnloadInline(admin.TabularInline):
#     model = Unload


class UnloadAdmin(ModelAdmin):
    date_hierarchy = 'datetime'
    list_display = (
        'datetime',
        'type',
        'him',
        'water',
        'cement',
        'breakstone',
        'sand',
    )
    ordering = ('datetime',)

    class Meta:
        model = Unload


class CarrierAdmin(ModelAdmin):
    # inlines = [UnloadInline]

    class Meta:
        model = Carrier


admin.site.register(Unload, UnloadAdmin)
admin.site.register(UnloadType)
admin.site.register(Carrier, CarrierAdmin)
